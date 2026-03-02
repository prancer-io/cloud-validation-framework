"""
Tests for snapshot chunking (split/merge) logic.

Validates that:
1. Large snapshots are correctly split into chunks on write
2. Chunks are correctly merged back into a single snapshot on read
3. Base snapshot names are correctly extracted from chunk names
4. The merge preserves all nodes from all chunks
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

import copy
import pytest


# ===================================================================
# 1. _merge_snapshot_chunks (validation.py)
# ===================================================================

class TestMergeSnapshotChunks:
    """Tests for processor.connector.validation._merge_snapshot_chunks."""

    def test_empty_docs_returns_empty_dict(self):
        from processor.connector.validation import _merge_snapshot_chunks
        assert _merge_snapshot_chunks([]) == {}

    def test_single_doc_returns_json(self):
        from processor.connector.validation import _merge_snapshot_chunks
        doc = {'name': 'snap_gen', 'json': {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 1}]}]}}
        result = _merge_snapshot_chunks([doc])
        assert result == doc['json']

    def test_single_doc_with_none_json(self):
        from processor.connector.validation import _merge_snapshot_chunks
        doc = {'name': 'snap_gen', 'json': None}
        result = _merge_snapshot_chunks([doc])
        assert result == {}

    def test_merge_two_chunks_same_source_type(self):
        from processor.connector.validation import _merge_snapshot_chunks
        base = {
            'name': 'TEST_gen',
            'json': {
                'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'node1'}, {'id': 'node2'}]}]
            }
        }
        part1 = {
            'name': 'TEST_gen_part1',
            'json': {
                'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'node3'}, {'id': 'node4'}]}]
            }
        }
        result = _merge_snapshot_chunks([base, part1])
        nodes = result['snapshots'][0]['nodes']
        assert len(nodes) == 4
        assert [n['id'] for n in nodes] == ['node1', 'node2', 'node3', 'node4']

    def test_merge_three_chunks(self):
        from processor.connector.validation import _merge_snapshot_chunks
        docs = []
        for i, name in enumerate(['TEST_gen', 'TEST_gen_part1', 'TEST_gen_part2']):
            docs.append({
                'name': name,
                'json': {
                    'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'node_%d' % i}]}]
                }
            })
        result = _merge_snapshot_chunks(docs)
        nodes = result['snapshots'][0]['nodes']
        assert len(nodes) == 3

    def test_merge_preserves_base_document_structure(self):
        from processor.connector.validation import _merge_snapshot_chunks
        base = {
            'name': 'TEST_gen',
            'json': {
                'fileType': 'snapshot',
                'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'n1'}]}],
                'extra_field': 'preserved'
            }
        }
        part1 = {
            'name': 'TEST_gen_part1',
            'json': {
                'fileType': 'snapshot',
                'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'n2'}]}]
            }
        }
        result = _merge_snapshot_chunks([base, part1])
        assert result['fileType'] == 'snapshot'
        assert result['extra_field'] == 'preserved'

    def test_merge_sorts_chunks_correctly(self):
        """Chunks should be merged in order: base, part1, part2, etc."""
        from processor.connector.validation import _merge_snapshot_chunks
        # Provide in reverse order to test sorting
        part2 = {'name': 'T_gen_part2', 'json': {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'c'}]}]}}
        base = {'name': 'T_gen', 'json': {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'a'}]}]}}
        part1 = {'name': 'T_gen_part1', 'json': {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'b'}]}]}}
        result = _merge_snapshot_chunks([part2, base, part1])
        nodes = result['snapshots'][0]['nodes']
        assert [n['id'] for n in nodes] == ['a', 'b', 'c']

    def test_merge_different_source_types(self):
        """Chunks with different source/type should be kept separate."""
        from processor.connector.validation import _merge_snapshot_chunks
        base = {
            'name': 'T_gen',
            'json': {
                'snapshots': [
                    {'source': 's1', 'type': 'aws', 'nodes': [{'id': 'aws1'}]},
                    {'source': 's2', 'type': 'azure', 'nodes': [{'id': 'az1'}]}
                ]
            }
        }
        part1 = {
            'name': 'T_gen_part1',
            'json': {
                'snapshots': [
                    {'source': 's1', 'type': 'aws', 'nodes': [{'id': 'aws2'}]}
                ]
            }
        }
        result = _merge_snapshot_chunks([base, part1])
        assert len(result['snapshots']) == 2
        aws_snap = [s for s in result['snapshots'] if s['type'] == 'aws'][0]
        azure_snap = [s for s in result['snapshots'] if s['type'] == 'azure'][0]
        assert len(aws_snap['nodes']) == 2
        assert len(azure_snap['nodes']) == 1

    def test_merge_chunk_with_new_source_type(self):
        """A chunk with a source/type not in base should be appended."""
        from processor.connector.validation import _merge_snapshot_chunks
        base = {
            'name': 'T_gen',
            'json': {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'n1'}]}]}
        }
        part1 = {
            'name': 'T_gen_part1',
            'json': {'snapshots': [{'source': 's2', 'type': 'google', 'nodes': [{'id': 'g1'}]}]}
        }
        result = _merge_snapshot_chunks([base, part1])
        assert len(result['snapshots']) == 2

    def test_merge_skips_empty_json_chunks(self):
        from processor.connector.validation import _merge_snapshot_chunks
        base = {
            'name': 'T_gen',
            'json': {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'n1'}]}]}
        }
        part1 = {'name': 'T_gen_part1', 'json': {}}
        part2 = {'name': 'T_gen_part2', 'json': None}
        result = _merge_snapshot_chunks([base, part1, part2])
        assert len(result['snapshots'][0]['nodes']) == 1


# ===================================================================
# 2. _get_base_snapshot_name (snapshot.py)
# ===================================================================

class TestGetBaseSnapshotName:
    """Tests for processor.connector.snapshot._get_base_snapshot_name."""

    def test_base_name_unchanged(self):
        from processor.connector.snapshot import _get_base_snapshot_name
        assert _get_base_snapshot_name('TEST_IAM_01_gen') == 'TEST_IAM_01_gen'

    def test_part1_returns_base(self):
        from processor.connector.snapshot import _get_base_snapshot_name
        assert _get_base_snapshot_name('TEST_IAM_01_gen_part1') == 'TEST_IAM_01_gen'

    def test_part99_returns_base(self):
        from processor.connector.snapshot import _get_base_snapshot_name
        assert _get_base_snapshot_name('TEST_IAM_01_gen_part99') == 'TEST_IAM_01_gen'

    def test_non_gen_name_unchanged(self):
        from processor.connector.snapshot import _get_base_snapshot_name
        assert _get_base_snapshot_name('some_snapshot') == 'some_snapshot'

    def test_gen_in_middle_not_affected(self):
        from processor.connector.snapshot import _get_base_snapshot_name
        # Only _gen at the end should be matched
        assert _get_base_snapshot_name('test_gen_something') == 'test_gen_something'


# ===================================================================
# 3. _split_snapshot_nodes (master_snapshot.py)
# ===================================================================

class TestSplitSnapshotNodes:
    """Tests for processor.crawler.master_snapshot._split_snapshot_nodes."""

    def test_small_doc_returns_single_element(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        doc = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'n1'}]}]}
        result = _split_snapshot_nodes(doc)
        assert len(result) == 1
        assert result[0] is doc

    def test_empty_snapshots_returns_single(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        doc = {'snapshots': []}
        result = _split_snapshot_nodes(doc)
        assert len(result) == 1

    def test_no_nodes_returns_single(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        doc = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': []}]}
        result = _split_snapshot_nodes(doc)
        assert len(result) == 1

    def test_split_produces_multiple_chunks(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        # Create a document with many nodes that will exceed a very small max_size
        nodes = [{'id': 'node_%d' % i, 'data': 'x' * 100} for i in range(50)]
        doc = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': nodes}]}
        result = _split_snapshot_nodes(doc, max_size=500)
        assert len(result) > 1
        # All nodes should be present across all chunks
        all_nodes = []
        for chunk in result:
            for snap in chunk['snapshots']:
                all_nodes.extend(snap['nodes'])
        assert len(all_nodes) == 50

    def test_split_preserves_all_node_ids(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        nodes = [{'id': 'node_%d' % i, 'data': 'x' * 100} for i in range(20)]
        doc = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': nodes}]}
        result = _split_snapshot_nodes(doc, max_size=500)
        all_ids = set()
        for chunk in result:
            for snap in chunk['snapshots']:
                for node in snap['nodes']:
                    all_ids.add(node['id'])
        expected_ids = {'node_%d' % i for i in range(20)}
        assert all_ids == expected_ids

    def test_split_each_chunk_has_valid_structure(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        nodes = [{'id': 'n_%d' % i, 'data': 'x' * 200} for i in range(30)]
        doc = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': nodes}]}
        result = _split_snapshot_nodes(doc, max_size=500)
        for chunk in result:
            assert 'snapshots' in chunk
            assert isinstance(chunk['snapshots'], list)
            assert len(chunk['snapshots']) > 0
            for snap in chunk['snapshots']:
                assert 'nodes' in snap
                assert len(snap['nodes']) > 0


# ===================================================================
# 4. Round-trip: split then merge preserves all data
# ===================================================================

class TestSplitMergeRoundTrip:
    """Verify that splitting then merging preserves all nodes."""

    def test_roundtrip_all_nodes_preserved(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        from processor.connector.validation import _merge_snapshot_chunks

        nodes = [{'id': 'node_%d' % i, 'snapshotId': 'snap_%d' % i, 'data': 'x' * 200} for i in range(40)]
        original = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': nodes}]}

        # Split
        chunks = _split_snapshot_nodes(original, max_size=500)
        assert len(chunks) > 1

        # Simulate DB storage with naming
        docs = []
        for idx, chunk in enumerate(chunks):
            name = 'TEST_gen' if idx == 0 else 'TEST_gen_part%d' % idx
            docs.append({'name': name, 'json': chunk})

        # Merge
        merged = _merge_snapshot_chunks(docs)
        merged_nodes = merged['snapshots'][0]['nodes']
        assert len(merged_nodes) == 40
        merged_ids = {n['id'] for n in merged_nodes}
        original_ids = {n['id'] for n in nodes}
        assert merged_ids == original_ids

    def test_roundtrip_single_chunk_no_split(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        from processor.connector.validation import _merge_snapshot_chunks

        original = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': [{'id': 'n1'}]}]}
        chunks = _split_snapshot_nodes(original)
        assert len(chunks) == 1

        docs = [{'name': 'TEST_gen', 'json': chunks[0]}]
        merged = _merge_snapshot_chunks(docs)
        assert merged['snapshots'][0]['nodes'] == [{'id': 'n1'}]

    def test_roundtrip_preserves_node_order_within_chunks(self):
        from processor.crawler.master_snapshot import _split_snapshot_nodes
        from processor.connector.validation import _merge_snapshot_chunks

        nodes = [{'id': 'node_%03d' % i, 'data': 'x' * 200} for i in range(30)]
        original = {'snapshots': [{'source': 's1', 'type': 'aws', 'nodes': nodes}]}

        chunks = _split_snapshot_nodes(original, max_size=500)
        docs = []
        for idx, chunk in enumerate(chunks):
            name = 'T_gen' if idx == 0 else 'T_gen_part%d' % idx
            docs.append({'name': name, 'json': chunk})

        merged = _merge_snapshot_chunks(docs)
        merged_ids = [n['id'] for n in merged['snapshots'][0]['nodes']]
        # Nodes within each chunk should maintain order, and chunks are in order
        # So the merged result should be the same as original
        original_ids = [n['id'] for n in nodes]
        assert merged_ids == original_ids
