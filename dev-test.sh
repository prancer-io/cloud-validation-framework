python -m pip install --upgrade pip && pip install -r requirements.txt
export BASEDIR=`pwd`
export FRAMEWORKDIR=`pwd`
export PYTHONPATH=$FRAMEWORKDIR/src
python utilities/validator.py --help
py.test --cov=processor tests/processor --cov-report term-missing
if [ $? -ne 0 ]; then echo "Unit tests failed"; exit 1; fi
git clone https://github.com/prancer-io/prancer-hello-world.git
cd $BASEDIR/prancer-hello-world
export FRAMEWORKDIR=`pwd`
cd $BASEDIR
python utilities/validator.py --db NONE scenario-pass
pass_success=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-pass/output-test.json`
fail_error=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-pass/output-test.json`
if [[ -z "$pass_success" ]] || [[ ! -z "$failed_error" ]] ; then   echo "scenario-pass failed"; exit 1;fi
python utilities/validator.py --db NONE scenario-fail
fail_success=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-fail/output-test.json`
pass_error=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-fail/output-test.json`
if [[ -z "$fail_success" ]] || [[ ! -z "$pass_error" ]] ; then   echo "scenario-fail failed"; exit 1;fi
exit 0
