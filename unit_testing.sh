python -m pip install --upgrade pip && pip install -r requirements.txt
pip install pymongo
export BASEDIR=`pwd`
export FRAMEWORKDIR=`pwd`
export PYTHONPATH=$FRAMEWORKDIR/src
python utilities/validator.py --help
py.test --cov=processor tests/processor --cov-report term-missing

export FRAMEWORKDIR=`pwd`
cd $BASEDIR
git clone https://github.com/prancer-io/prancer-hello-world.git
cd $BASEDIR/prancer-hello-world
export FRAMEWORKDIR=`pwd`
cd $BASEDIR
python utilities/validator.py --db NONE scenario-pass
cd $BASEDIR/prancer-hello-world/validation/scenario-pass/
pass_error=`grep passed output-test.json`n
cd $BASEDIR
python utilities/validator.py --db NONE scenario-fail
cd $BASEDIR/prancer-hello-world/validation/scenario-fail/
fail_error=`grep failed output-test.json`
echo pass_error = $pass_error
echo fail_error = $fail_error
if [ -z "$pass_error" ] && [ -z "$fail_error" ]
then
      echo "Variables contains one of them or both empty, failing tests"
else
      echo "Variables are NOT empty, passing tests"
      return 0
fi