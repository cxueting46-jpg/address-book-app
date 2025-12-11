from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///address_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 用于flash消息
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    social_media = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    favorite = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    # 获取所有联系人，星标联系人排在最前面
    contacts = Contact.query.order_by(Contact.favorite.desc(), Contact.name.asc()).all()
    return render_template('index.html', contacts=contacts)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    new_contact = Contact(
        name=request.form['name'],
        phone=request.form['phone'],
        email=request.form['email'],
        social_media=request.form['social_media'],
        address=request.form['address'],
        notes=request.form['notes']
    )
    db.session.add(new_contact)
    db.session.commit()
    flash(f'✅ Contact "{new_contact.name}" added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/favorite/<int:contact_id>')
def favorite(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    contact.favorite = not contact.favorite  # Toggle favorite status

    if contact.favorite:
        flash(f'⭐ "{contact.name}" added to favorites!', 'success')
    else:
        flash(f'📌 "{contact.name}" removed from favorites.', 'info')

    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_contact/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        contact.social_media = request.form['social_media']
        contact.address = request.form['address']
        contact.notes = request.form['notes']
        db.session.commit()
        flash(f'✏️ Contact "{contact.name}" updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contact)


@app.route('/delete_contact/<int:contact_id>')
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    contact_name = contact.name
    db.session.delete(contact)
    db.session.commit()
    flash(f'🗑️ Contact "{contact_name}" deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/export')
def export_contacts():
    contacts = Contact.query.order_by(Contact.favorite.desc(), Contact.name.asc()).all()
    data = [{'Name': c.name, 'Phone': c.phone, 'Email': c.email,
             'Social Media': c.social_media, 'Address': c.address,
             'Notes': c.notes, 'Favorite': '⭐' if c.favorite else ''} for c in contacts]
    df = pd.DataFrame(data)

    # 创建内存中的Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contacts')

    output.seek(0)

    # 发送文件给用户下载
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='contacts.xlsx'
    )


@app.route('/import', methods=['POST'])
def import_contacts():
    if 'file' not in request.files:
        flash('❌ No file uploaded.', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file:
        try:
            df = pd.read_excel(file)
            count = 0
            for _, row in df.iterrows():
                # 处理Favorite列（可能为空或包含⭐）
                favorite = False
                if 'Favorite' in row:
                    fav_value = row['Favorite']
                    if isinstance(fav_value, str) and '⭐' in fav_value:
                        favorite = True
                    elif isinstance(fav_value, bool):
                        favorite = fav_value

                contact = Contact(
                    name=row['Name'],
                    phone=row.get('Phone', ''),
                    email=row.get('Email', ''),
                    social_media=row.get('Social Media', ''),
                    address=row.get('Address', ''),
                    notes=row.get('Notes', ''),
                    favorite=favorite
                )
                db.session.add(contact)
                count += 1
            db.session.commit()
            flash(f'✅ Successfully imported {count} contacts!', 'success')
        except Exception as e:
            flash(f'❌ Error importing file: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():  # 进入应用上下文
        db.create_all()  # 创建数据库表
    app.run(debug=True)