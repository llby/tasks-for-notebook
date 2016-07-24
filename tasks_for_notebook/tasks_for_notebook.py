import os
import pandas
from IPython.display import Javascript
from IPython.display import HTML

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
  df = pandas.DataFrame([{'name':name,'content':content,'status':'new'}], columns = ['name','content','status'])
  data = data.append(df, ignore_index=True)
  save_task(data)

def show_task():
  data = read_task()
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
  return HTML('<h2>%s</h2>'%(title_name) + data.to_html() + js)

def update_task(id, **kwargs):
  data = read_task()
  if kwargs.get('name'):
    data['name'][id] = kwargs.get('name')
  if kwargs.get('content'):
    data['content'][id] = kwargs.get('content')
  if kwargs.get('status'):
    data['status'][id] = kwargs.get('status')
  save_task(data)

def delete_task(id):
  data = read_task()
  data = data.drop(id)
  save_task(data)
