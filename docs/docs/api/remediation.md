**Remediation APIs**
===

- Remediation is feature for auto fix any security related issue in Pre deployment template files or fix the configuration on cloud resources post deployment.

**Remediation - Run**
---

**CURL Sample**
```
curl -X POST https://portal.prancer.io/prancer-customer1/api/remediate/testcase/' -H 'authorization: Bearer <JWT Bearer Token>' -H 'content-type: application/json' -d '{ "output_id":"608d646f32e86e9c9453c665", "snapshot_id":"ARM_TEMPLATE_SNAPSHOT10", "remediation_id":"PR-AZR-0053-ARM" }'
```

- **URL:** https://portal.prancer.io/prancer-customer1/api/remediate/testcase/
- **Method:** POST
- **Header:**
```
    - content-type: application/json
    - Authorization: Bearer <JWT Bearer Token>
```
- **Param:**
```
{
	output_id: "608d646f32e86e9c9453c665",
    remediation_id: "PR-AZR-0053-ARM",
    snapshot_id: "ARM_TEMPLATE_SNAPSHOT10"
}
```
- **Explanation:**

    `Required Fields`

    - **output_id:** Object Id of output collection for which you want to run remediation.
    - **snapshot_id:** A valid snapshotId which should be contains in output object.
    - **remediation_id:** Valid predefined remediation Id. Remediation will be apply on resource which will be refer from provided snapshot Id.

 
**Response:**
```
{
    "data": {
        "url": "https://github.com/<gitusername>/<repository_name>/pull/151"
    },
    "error": "",
    "error_list": [],
    "message": "Remediation completed",
    "metadata": {},
    "status": 200
}
```
