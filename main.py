import pymysql
from config import mysql
from config import app
from flask import flash, render_template, request, redirect

from flask_table import Table, Col, LinkCol
 
class Results(Table):
    student_id = Col('Id', show=False)
    student_name = Col('Имя')
    student_surname = Col('Фамилия')
    student_email = Col('Email')
    student_group = Col('Группа')
    edit = LinkCol('Изменить', 'edit_view', url_kwargs=dict(id='student_id'))
    delete = LinkCol('Удалить', 'delete_student', url_kwargs=dict(id='student_id'))


@app.route('/new_student')
def add_student_view():
	return render_template('add.html')

@app.route('/add', methods=['POST'])
def add_student():
	try:
		_name = request.form['inputName']
		_surname = request.form['inputSurname']
		_email = request.form['inputEmail']
		_group = request.form['inputGroup']
		# validate the received values
		if _name and _surname and _email and _group and request.method == 'POST':
			sql = "INSERT INTO student_table(student_name, student_surname, student_email, student_group) VALUES(%s, %s, %s, %s)"
			data = (_name, _surname, _email, _group,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Информация добавлена успешно!')
			return redirect('/')
		else:
			return 'Ошибка при добавлении информации!'
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/')
def students():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM student_table")
		rows = cursor.fetchall()
		table = Results(rows)
		table.border = True
		return render_template('students.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/edit/<int:id>')
def edit_view(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM student_table WHERE student_id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit.html', row=row)
		else:
			return 'Ошибка загрузки #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update', methods=['POST'])
def update_student():
	try:
		_name = request.form['inputName']
		_surname = request.form['inputSurname']
		_email = request.form['inputEmail']
		_group = request.form['inputGroup']
		_id = request.form['id']
		# validate the received values
		if _name and _surname and _email and _group and _id and request.method == 'POST':
			sql = "UPDATE student_table SET student_name=%s, student_surname=%s, student_email=%s, student_group=%s WHERE student_id=%s"
			data = (_name, _surname, _email, _group, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('Информация обновлена успешно!')
			return redirect('/')
		else:
			return 'Ошибка при обновлении информации'
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/delete/<int:id>')
def delete_student(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM student_table WHERE student_id=%s", (id,))
		conn.commit()
		flash('Информация удалена успешно!')
		return redirect('/')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

if __name__ == "__main__":
    app.run()
