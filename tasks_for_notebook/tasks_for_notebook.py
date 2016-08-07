import os
import pandas
from IPython.display import Javascript
from IPython.display import HTML
from datetime import datetime

title_name = 'Tasks'
file_name = 'tasks.csv'
css_name = '//cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css'
js_name = '//cdn.datatables.net/1.10.12/js/jquery.dataTables.min'

def read_task():
  if os.path.exists(file_name):
    return pandas.DataFrame.from_csv(file_name)
  else:
    return pandas.DataFrame()

def save_task(data):
  pandas.DataFrame(data).to_csv(file_name)

def add_task(name, content):
  data = read_task()
  df = pandas.DataFrame([{
         'name':name,
         'content':content,
         'status':'new',
         'created_at':datetime.now().strftime("%Y/%m/%d %H:%M:%S")
       }], columns = ['name', 'content', 'status', 'created_at', 'updated_at'])
  data = data.append(df, ignore_index=True)
  save_task(data)

def render_task(data):
  js = '''
    <link rel='stylesheet' type='text/css' href='%s'>
    <script>
      require.config({
        paths: {
          dataTables: '%s'
        }
     });
      require(['dataTables'], function(){
        $('.dataframe').DataTable();
      });
    </script>
  '''%(css_name, js_name)
  return HTML('<h2>%s</h2>'%(title_name) + data.to_html(classes="display") + js)

def show_done_task():
  data = read_task()
  data = data[data['status'] == 'done']
  return render_task(data)

def show_task():
  data = read_task()
  data = data[data['status'] != 'done']
  return render_task(data)

def update_task(id, **kwargs):
  data = read_task()
  if kwargs.get('name'):
    data.loc.__setitem__((slice(id, id), 'name'), kwargs.get('name'))
  if kwargs.get('content'):
    data.loc.__setitem__((slice(id, id), 'content'), kwargs.get('content'))
  if kwargs.get('status'):
    data.loc.__setitem__((slice(id, id), 'status'), kwargs.get('status'))
  data.loc.__setitem__((slice(id, id), 'updated_at'), datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
  save_task(data)

def delete_task(id):
  data = read_task()
  data = data.drop(id)
  save_task(data)

def backup_task():
  os.system( "mkdir backup" )
  os.system( "cp %s backup/%s_%s"%(file_name, datetime.now().strftime("%Y%m%d%H%M%S"), file_name) )
