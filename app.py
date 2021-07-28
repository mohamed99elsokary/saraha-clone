from config import app

app.config["SECRET_KEY"] = "dk;vnjfvdfblkcvjn klasdanfivsndsj"

# ------------------------------users
from methods.users.sign_up import sign_up
from methods.users.login import login
from methods.users.logout import logout
from methods.users.reset_password import reset_password
from methods.users.edit_acc import edit_acc
from methods.users.delete import delete

# ------------------------------Comments
from methods.comments.add_comment import add_comment
from methods.comments.view_comments import view_comments
from methods.comments.delete_comment import delete_comment

# ------------------------------users
app.register_blueprint(delete)
app.register_blueprint(edit_acc)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(reset_password)
app.register_blueprint(sign_up)
# ------------------------------Comments
app.register_blueprint(add_comment)
app.register_blueprint(view_comments)
app.register_blueprint(delete_comment)

if __name__ == "__main__":
    app.run(debug=True)
