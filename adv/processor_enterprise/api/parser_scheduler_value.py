import sys
import datetime
from datetime import timedelta
from dateutil import parser
#from date_interpreter import IST

def parse_minutely(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'minute' : '*/1'}
   try:
      val = parse_minute(current_values[1])
      minute_val = int(val['minute'])
      if minute_val < 60:
         value['minute'] = '*/%d' % minute_val
   except Exception as ex:
      print("Exception: %s" % ex)
   return value

def parse_hourly(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'hour': '*/1', 'minute' : '10'}
   try:
      val = parse_minute(current_values[1])
      minute_val = int(val['minute'])
      if minute_val < 60:
         value['minute'] = '%d' % minute_val
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_daily(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'day': '*/1', 'hour': 9, 'minute' : 30}
   try:
      value.update(parse_time(current_values[1]))
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_weekly(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'day_of_week': '0', 'hour': '9', 'minute' : '30'}
   try:
      value.update(parse_time(current_values[1]))
      value["day_of_week"] = start_date.weekday()
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_monthly(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'month': '*/1', 'day': '1', 'hour': '9', 'minute' : '30'}
   try:
      value.update(parse_time(current_values[1]))
      value["day"] = start_date.strftime("%d")
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_quarterly(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'month': '*/3', 'day': '1', 'hour': '9', 'minute' : '30'}
   try:
      value.update(parse_time(current_values[1]))
      value["day"] = start_date.strftime("%d")
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_halfyearly(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'month': '*/6', 'day': '1', 'hour': '9', 'minute' : '30'}
   try:
      value.update(parse_time(current_values[1]))
      value["day"] = start_date.strftime("%d")
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_yearly(freq_str, start_date):
   current_values = freq_str.split('@')
   value = {'year': '*/1', 'month': '1', 'day': '1', 'hour': '9', 'minute': '30'}
   try:
      value.update(parse_time(current_values[1]))
      value["month"] = start_date.strftime("%m")
      value["day"] = start_date.strftime("%d")
   except Exception as ex:
      print("Execption: %s" % ex)
   return value

def parse_once(freq_str, date):
   current_values = freq_str.split('@')
   end_date = date + timedelta(seconds=10)
   if len(current_values) > 1 :
      try:
         val = int(current_values[1][:-1])
         if current_values[1].endswith('s'):
            #end_date = datetime.datetime.now(IST()) + timedelta(seconds=val)
            end_date = datetime.datetime.now() + timedelta(seconds=val)
         elif current_values[1].endswith('m'):
            #end_date = datetime.datetime.now(IST()) + timedelta(minutes=val)
            end_date = datetime.datetime.now() + timedelta(minutes=val)
         elif current_values[1].endswith('h'):
            #end_date = datetime.datetime.now(IST()) + timedelta(hours=val)
            end_date = datetime.datetime.now() + timedelta(hours=val)
         elif current_values[1].endswith('d'):
            #end_date = datetime.datetime.now(IST()) + timedelta(days=val)
            end_date = datetime.datetime.now() + timedelta(days=val)
      except Exception as ex:
        date_str = "%s %s" % (date.strftime("%d/%m/%Y"), current_values[1])
        #end_date = parser.parse(date_str, dayfirst=True).replace(tzinfo = IST())
        end_date = parser.parse(date_str, dayfirst=True)
        if end_date is None:     
           #end_date = datetime.datetime.now(IST()) + timedelta(seconds=10)
           end_date = datetime.datetime.now() + timedelta(seconds=10)
   value = {'run_date': end_date}
   return value

values = {'minutely': parse_minutely, 'hourly': parse_hourly,
          'daily': parse_daily, 'weekly': parse_weekly,
          'monthly': parse_monthly, 'quarterly': parse_quarterly,
          'halfyearly': parse_halfyearly, 'yearly': parse_yearly,
          'once': parse_once
         }

def parse_time(time_str):
   val = {"hour": "9", "minute": "30"}
   try:
      time_vals = time_str.split(':')
      if len(time_vals) > 0:
         given_hour = int(time_vals[0])
         if given_hour < 24:
            val["hour"] = "%d" % given_hour
      if len(time_vals) > 1:
         given_minute = int(time_vals[1])
         if given_minute < 60:
            val["minute"] = "%d" % given_minute
   except Exception as ex:
      pass
   return val

def parse_minute(time_str):
   val = {"minute": "30"}
   try:
      if time_str:
         given_minute = int(time_str)
         if given_minute < 60:
            val["minute"] = "%d" % given_minute
   except Exception as ex:
      pass
   return val

def main():
   if len(sys.argv) > 1:
      input_str = " ".join(sys.argv[1:])
      print(input_str)
      val = parse_value(input_str)
      print(val)
   else:
      print("Invalid: give some input string")

def parse_value(current_value):
   value = {}
   vals = current_value.lower().split(' ')
   freq_str = None
   freq_function = None
   start_date = None
   for val in vals:
      freq_vals = val.split("@")
      if freq_vals and freq_vals[0].lower() in values:
         freq_function = values[freq_vals[0]]
         freq_str = val
      elif freq_vals[0] == "date" :
         #start_date = parser.parse(freq_vals[1], dayfirst=True).replace(tzinfo = IST())
         start_date = parser.parse(freq_vals[1], dayfirst=True)
   if start_date is None:
      #start_date = datetime.datetime.now(IST()) + timedelta(seconds=10)
      start_date = datetime.datetime.now() + timedelta(seconds=10)
   if freq_str and freq_function:
      value = freq_function(freq_str, start_date)
   return start_date, value

if __name__ == '__main__':
   main()

