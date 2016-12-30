# -*- coding: utf-8 -*-
# try something like
import datetime
import fuct
def registration():
    fields=['wpa_member', 'usaa_member', 'date_of_birth', 'bow', 'joad_indoor', 'joad_outdoor', 'adult_indoor', 'adult_outdoor', 'inclusive']
    fn= {'wpa_member':'WPA Member Number', 
         'usaa_member':'USAA Member Number', 
         'bow':'Bow Type', 
         'joad_indoor':'Star Award Level Joad Indoor',
         'joad_outdoor':'Star Award Level Joad Outdoor', 
         'adult_indoor':'Star Award Level Adult Indoor', 
         'adult_outdoor':'Star Award Adult Outdoor',
         'inclusive':'Inclusive Enrollment'}
    r = db(db.joad_registration.wpa_member == session.memId).select().first()
    form = SQLFORM(db.joad_registration, record=r, submit_button='Next', fields=fields, labels=fn)
    form.vars.wpa_member = session.memId
    form.vars.date_of_birth = request.args[1]
    if form.process().accepted:
        row = db(db.joad_registration.wpa_member == session.memId).select().first()
        row.expire_date = fuct.calc_expire(row.expire_date)
        row.update_record()
        redirect(URL('default', request.args[0]))

    return dict(grid=form)
def pin_shoot(): 
    return dict(grid=SQLFORM.grid(db.pin_shoot, deletable=False, exportclasses=export_classes))
