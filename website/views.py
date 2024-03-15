from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from .models import Todo, Category
from sqlalchemy import func
from .database import db


my_view = Blueprint("my_view", __name__)

def add_common_categories():
    common_categories = ["Personal", "Work", "Study", "Fitness", "Home", "Errands", "Social", "Finances", "Health", "Family"]
    for category_name in common_categories:
        existing_category = Category.query.filter_by(name=category_name).first()
        if not existing_category:
            category = Category(name=category_name)
            db.session.add(category)
    db.session.commit()
    
@my_view.route("/")
def home():
    try:
        todo_list = Todo.query.filter_by(complete=False).all()
        completed_count = Todo.query.filter_by(complete=True).count()
        categories = Category.query.all()  # Fetch all categories
        message = request.args.get('message', None)
        success_message = request.args.get('success_message', None)
        return render_template("index.html", todo_list=todo_list, message=message, success_message=success_message, completed_count=completed_count, categories=categories)
    except Exception as e:
        error_message = "An error occurred while loading the home page: " + str(e)
        return render_template("error.html", error_message=error_message)


@my_view.route("/add", methods=['POST'])
def add():
    try:
        task = request.form.get("task")
        task_lower = task.lower()
        existing_task = Todo.query.filter(func.lower(Todo.task) == task_lower).first()
        if existing_task:
            message = "This task already exists!"
            return redirect(url_for('my_view.home', message=message))
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        success_message = "Task added successfully!"
        return redirect(url_for('my_view.home', success_message=success_message))
    except:
        error_message = "There was an error adding your task"
        return redirect(url_for('my_view.home', error_message=error_message))

#update the list to mark it as complete
@my_view.route("/update/<todo_id>", methods=['POST'])
def update(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if todo:
            # Toggle the complete status of the task
            todo.complete = not todo.complete
            db.session.commit()
            flash("Task status updated successfully!", "success")
            
            if todo.complete:
                # Move completed task to completed tasks page
                return redirect(url_for('my_view.completed_tasks'))
        else:
            flash("Task not found", "error")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
    return redirect(url_for('my_view.home'))

@my_view.route("/completed_tasks")
def completed_tasks():
    completed_todo_list = Todo.query.filter_by(complete=True).all()
    return render_template("completed_tasks.html", completed_todo_list=completed_todo_list)

#delete a task from the list
@my_view.route("/delete/<todo_id>", methods=['GET', 'POST'])
def delete(todo_id):
    if request.method == 'POST':
        try:
            todo = Todo.query.filter_by(id=todo_id).first()
            db.session.delete(todo)
            db.session.commit()
            success_message = "Task deleted successfully!"
            return redirect(url_for('my_view.home', success_message=success_message))
        except:
            error_message = "There was an error deleting the task"
            return redirect(url_for('my_view.home', error_message=error_message))
    else:
        error_message = "Method Not Allowed"
        return redirect(url_for('my_view.home', error_message=error_message))

@my_view.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message="Page not found"), 404

@my_view.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_message="Internal server error"), 500