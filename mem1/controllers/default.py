# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import datetime
import mem1email
import fuct

export_classes = dict(csv=True, json=False, html=False,
                  tsv=False, xml=False, csv_with_hidden_cols=False,
                  tsv_with_hidden_cols=False)
def index():
    session.familyId = 0
    session.memId = 0
    tbl1 = TABLE(TR(TH("WPA")), TR(A('New Member', _href=URL('newmember_form', args=[0]))),
                TR(A('Renewal', _href=URL('get_id'))),
                TR(A('List', _href=URL('list_members'))),
                TR(A('Instructor', _href=URL('instructor'))))
    tbl2 = TABLE(TR(TH("JOAD/AAP")), TR(A('Registration', _href=URL('joad_ctrl', 'registration'))),
                TR(A('Pin Shoot', _href=URL('joad_ctrl', 'pin_shoot'))))
    return dict(tbl1=tbl1, tbl2=tbl2)

@auth.requires_login()
def get_id():
    # this seems like the wrong way to get an id but ...
    #form = SQLFORM(db.addr, submit_button='Next', fields=['zip'], labels={'zip':'id'}, showid=True)
    form = FORM('Your id:', INPUT(_name='number', requires=IS_NOT_EMPTY()), INPUT(_type='submit'))
    if form.accepts(request,session):
        redirect(URL('newmember_form', args=(form.vars.number)))
        #redirect(URL('form2', args=(form.vars.id, True)))
    return dict(form=form)
@auth.requires_login()
def instructor():
    return dict(grid=SQLFORM.grid(db.instructor, deletable=False, exportclasses=export_classes))
@auth.requires_login()
def list_members():
    return dict(grid=SQLFORM.grid(db.addr, deletable=False, exportclasses=export_classes))
@auth.requires_login()
def newmember_form():
    fields=["first_name",'last_name','street','city','state','zip','cell','phone','email','birth_date','wpa_joad']
    if(int(request.args[0]) > 0):
        row = db(db.addr.id == request.args[0]).select().first()
        session.familyId = int(row.family)
        form = SQLFORM(db.addr, row, submit_button='Next', fields=fields)
    else:
        form = SQLFORM(db.addr, submit_button='Next', fields=fields)
        
        if(session.memId != 0): # if we are adding a family member
            row = db(db.addr.id == session.memId).select().first()
#             form.vars.first_name = row.first_name
#             form.vars.last_name = row.last_name
            form.vars.street = row.street
            form.vars.city = row.city
            form.vars.state = row.state
            form.vars.zip = row.zip
            form.vars.cell = row.cell
            form.vars.phone = row.phone
            form.vars.email = row.email
            form.vars.birth_date = row.birth_date
    if form.process().accepted:
        response.flash = 'form accepted'
        row = db(db.addr.id == form.vars.id).select().first()
        row.expire_date = fuct.calc_expire(row.expire_date)
        row.email_works = False
        row.family = session.familyId
        if(form.vars.email != ""):
            row.email_works = True
        row.update_record()
        if(session.familyId > 0):
            if(form.vars.wpa_joad):
                redirect(URL('joad_ctrl', 'registration', args=('form3', form.vars.birth_date)))#URL('joad_ctrl', 'registration', args=('form3')))
            else: redirect(URL('form3'))
        else:
            if(session.memId == 0): session.memId = form.vars.id
            if(form.vars.wpa_joad):
                redirect(URL('joad_ctrl', 'registration', args=('form2', form.vars.birth_date)))#URL('joad_ctrl', 'registration', args=('form2')))
            else: redirect(URL('form2'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        pass #response.flash = 'please fill out the form'
    return dict(form=form)
@auth.requires_login()
def form2():
    form = SQLFORM(db.form_update)
    form.vars.member_id = session.memId
#    form.vars.app_date = datetime.date.today().isoformat()
    form.vars.fam_bool = True
    if(session.familyId == 0):
        form.vars.fam_bool = False
    row = db(db.addr.id == session.memId).select().first()

    #else: form.vars.fam_bool = True #(session.familyid !=0)
    if form.process().accepted:
        response.flash = 'form accepted'
        if(form.vars.fam_bool):
        #if(form.vars.level == 'Family'):
            if(row.family == 0): #maybe 0
                m = db().select(db.addr.id, db.addr.family, orderby=db.addr.family).last().family
                row.family = m+1
                session.familyId = int(row.family)
                row.update_record()
                response.flash = session.familyId
            redirect(URL('form3'))
        if(row.email_works == True):
            mem1email.join_email([session.memId], [row.first_name], 'sam.amundson@gmail.com', request.folder)
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        pass #response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def form3():
#     form1 = famFormCreate(request.args[0])
    form_1 = FORM('Add Family Member:', INPUT(_type='submit'))
    form_2 = FORM("Finished", INPUT(_type='submit',_value = 'Save'))
    famlist = [["First", "Last", "Edit", "Delete"]]
    famId = []
    famName = []
    famdict = {}
    if(session.familyId > 0):
        for row in db(db.addr.family == session.familyId).select():
            famId.append(int(row.id))
            famName.append(row.first_name)
            if(row.id != session.memId):
                famdict[row.id]= [row.first_name, row.last_name, A("Edit", _href=URL(newmember_form,args=[row.id, 'family_member'])), A("Remove", _href=URL(removeFamilyMember,args=[row.id]))]
#             famlist.append([row.first_name, row.last_name, 'None','None'])
                            #A(str(row.id), _href=URL(newmember_form, vars=(row.id))), 'None'])
    
    if form_1.process(formname='form_one').accepted:
        response.flash = "form_1"
        redirect(URL('newmember_form', args=(0)))
    if form_2.process(formname='form_two').accepted:
        response.flash = "form_2"
        mem1email.join_email(famId, famName, 'sam.amundson@gmail.com', request.folder, True)
        redirect(URL('index'))
    return dict(form_1=form_1, form=famdict, form_2=form_2)#, add=A('Add Family Member', _href=URL('newmember_form', args=[0])))


def famFormCreate(memId):
    form = SQLFORM(db.addr, submit_button='Submit', fields=["first_name",'last_name','birth_date'])
    row = db(db.addr.id == memId).select().first()
    form.vars.street = row.street
    form.vars.city = row.city
    form.vars.state = row.state
    form.vars.zip = row.zip
    form.vars.cell = row.cell
    form.vars.phone = row.phone
    form.vars.email = row.email
    return form
# def famFormWork(form):
#     row = db(db.addr.id == form.vars.id).select().first()
#     row.expire_date = datetime.datetime.now() + datetime.timedelta(365)
#     row.email_works = True
#     row.update_record()
def removeFamilyMember():
    row = db(db.addr.id == request.args[0]).select().first()
    row.family = 0
    row.update_record()
    redirect(URL('form3'))
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
# def registration():
#     return dict(grid=SQLFORM.grid(db.joad_registration, deletable=False))

# def pin_shoot(): 
#     return dict(grid=SQLFORM.grid(db.pin_shoot, deletable=False))
