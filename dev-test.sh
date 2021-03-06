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
#scenario simple pass and fail
python utilities/validator.py --db NONE scenario-pass
pass_success=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-pass/output-test.json`
fail_error=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-pass/output-test.json`
if [[ -z "$pass_success" ]] || [[ ! -z "$failed_error" ]] ; then   echo "scenario-pass failed"; exit 1;fi
python utilities/validator.py --db NONE scenario-fail
fail_success=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-fail/output-test.json`
pass_error=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-fail/output-test.json`
if [[ -z "$fail_success" ]] || [[ ! -z "$pass_error" ]] ; then   echo "scenario-fail failed"; exit 1;fi
#scenario arm
python utilities/validator.py --db NONE scenario-arm-pass --crawler
python utilities/validator.py --db NONE scenario-arm-pass
pass_success=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-arm-pass/output-master-test.json`
fail_error=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-arm-pass/output-master-test.json`
if [[ -z "$pass_success" ]] || [[ ! -z "$failed_error" ]] ; then   echo "scenario-arm-pass failed"; exit 1;fi
python utilities/validator.py --db NONE scenario-arm-fail --crawler
python utilities/validator.py --db NONE scenario-arm-fail
fail_success=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-arm-fail/output-master-test.json`
pass_error=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-arm-fail/output-master-test.json`
if [[ -z "$fail_success" ]] || [[ ! -z "$pass_error" ]] ; then   echo "scenario-arm-fail failed"; exit 1;fi
#scenario cloudformation
python utilities/validator.py --db NONE scenario-cloudformation-pass --crawler
python utilities/validator.py --db NONE scenario-cloudformation-pass
pass_success=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-cloudformation-pass/output-master-test.json`
fail_error=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-cloudformation-pass/output-master-test.json`
if [[ -z "$pass_success" ]] || [[ ! -z "$failed_error" ]] ; then   echo "scenario-cloudformation-pass failed"; exit 1;fi
python utilities/validator.py --db NONE scenario-cloudformation-fail --crawler
python utilities/validator.py --db NONE scenario-cloudformation-fail
fail_success=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-cloudformation-fail/output-master-test.json`
pass_error=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-cloudformation-fail/output-master-test.json`
if [[ -z "$fail_success" ]] || [[ ! -z "$pass_error" ]] ; then   echo "scenario-cloudformation-fail failed"; exit 1;fi
#scenario deploymentmanager
python utilities/validator.py --db NONE scenario-deploymentmanager-pass --crawler
python utilities/validator.py --db NONE scenario-deploymentmanager-pass
pass_success=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-deploymentmanager-pass/output-master-test.json`
fail_error=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-deploymentmanager-pass/output-master-test.json`
if [[ -z "$pass_success" ]] || [[ ! -z "$failed_error" ]] ; then   echo "scenario-deploymentmanager-pass failed"; exit 1;fi
python utilities/validator.py --db NONE scenario-deploymentmanager-fail --crawler
python utilities/validator.py --db NONE scenario-deploymentmanager-fail
fail_success=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-deploymentmanager-fail/output-master-test.json`
pass_error=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-deploymentmanager-fail/output-master-test.json`
if [[ -z "$fail_success" ]] || [[ ! -z "$pass_error" ]] ; then   echo "scenario-deploymentmanager-fail failed"; exit 1;fi
#scenario kubernetes
python utilities/validator.py --db NONE scenario-kubernetes-pass --crawler
python utilities/validator.py --db NONE scenario-kubernetes-pass
pass_success=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-kubernetes-pass/output-master-test.json`
fail_error=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-kubernetes-pass/output-master-test.json`
if [[ -z "$pass_success" ]] || [[ ! -z "$failed_error" ]] ; then   echo "scenario-kubernetes-pass failed"; exit 1;fi
python utilities/validator.py --db NONE scenario-kubernetes-fail --crawler
python utilities/validator.py --db NONE scenario-kubernetes-fail
fail_success=`grep failed $BASEDIR/prancer-hello-world/validation/scenario-kubernetes-fail/output-master-test.json`
pass_error=`grep passed $BASEDIR/prancer-hello-world/validation/scenario-kubernetes-fail/output-master-test.json`
if [[ -z "$fail_success" ]] || [[ ! -z "$pass_error" ]] ; then   echo "scenario-kubernetes-fail failed"; exit 1;fi

chmod -R 777 $BASEDIR

exit 0
