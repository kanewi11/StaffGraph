from StaffGrapf import db, create_app

db.create_all(app=create_app())
app = create_app()
app.run(host='0.0.0.0', port='5005', debug=True)
