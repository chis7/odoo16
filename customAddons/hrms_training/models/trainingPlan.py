# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _, SUPERUSER_ID
import random


class TrainingPlan(models.Model):
    _name = "training.plan"
    _inherit = ["mail.thread"]
    _description = "training plan"
    # name = fields.Char(string="Ministry", required=True)
    name = fields.Many2one("res.company", string="Ministry")
    province = fields.Many2one("training.province", string="Province")
    # province = fields.Char(string="Province", required=True)
    institution = fields.Char(string="Institution", required=True)
    yearOfPlan = fields.Char(string="Year", required=True)
    supervisor_id = fields.Many2one("hr.employee", string="Supervisor")
    reference = fields.Char(
        string="Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    training_plan_line_ids = fields.One2many('training.plan.lines', 'training_plan_id', string="Training Plan Lines")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("hrdc", "HRDC"),
            ("ps", "PS"),
            ("psmd", "PSMD"),
            ("approved", "Approved"),
        ],
        default='draft',
        string="Status",
        required=True,
        tracking=True
    )
    hrdcComment = fields.Text(string="HRDC Comment", tracking=True)
    psComment = fields.Text(string="PS Comment", tracking=True)
    psmdComment = fields.Text(string="PSMD Comment", tracking=True)

    def action_save_training_plan_as_draft(self):
        self.write({'state': 'draft'})

    def action_submit_training_plan_to_hrdc(self):
        self.write({'state': 'hrdc'})


        group = self.env.ref("training.TrainingPlanHRDC")

        # Fetch users in the group
        users = group.users

        # Randomly select one user
        if users:
            selected_user = random.choice(users)

            # Assuming you have an email template
            # email_template_xml_id = 'your_module.email_template_xml_id'
            # email_template = self.env.ref(email_template_xml_id)

            # Send email to the selected user
            if selected_user.email:

                # Sending email
                mail_values = {
                    'subject': 'Request for Approval - Yourself',
                    'body_html': """<p>You have received a request for approval of a training plan. Click <a href='http://localhost:8069'>here</a> to log in and access the request.</p>""",
                    'email_to': selected_user.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()

            else:
                # Handle case where selected user does not have an email
                pass
        else:
            # Handle case where no users are in the group
            pass

    def action_hrdc_approve_training_plan(self):
        self.write({'state': 'ps'})

    def action_hrdc_send_back_training_plan(self):
        self.write({'state': 'draft'})

    def action_ps_approve_training_plan(self):
        self.write({'state': 'psmd'})

    def action_ps_send_back_training_plan(self):
        self.write({'state': 'hrdc'})

    def action_psmd_approve_training_plan(self):
        self.write({'state': 'approved'})

        for line in self.training_plan_line_ids:
            employee = line.employee_id
            if employee.user_id and employee.user_id.email:
                # Sending email
                mail_values = {
                    'subject': 'Approved Training - '+ employee.name,
                    'body_html': """<p>You have been shortlisted to attend a training and your training program has been approved.</p><p> Click <a href='http://localhost:8069'>here</a> to log in and access the request.</p>""",
                    'email_to': employee.user_id.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()

    def action_psmd_send_back_training_plan(self):
        self.write({'state': 'ps'})

    def send_email_to_random_user_in_group(self):
        # Replace 'your_group_xml_id' with the actual XML ID of the group
        group_xml_id = 'your_group_xml_id'
        group = self.env.ref(group_xml_id)

        # Fetch users in the group
        users = group.users

        # Randomly select one user
        if users:
            selected_user = random.choice(users)

            # Assuming you have an email template
            # email_template_xml_id = 'your_module.email_template_xml_id'
            # email_template = self.env.ref(email_template_xml_id)

            # Send email to the selected user
            if selected_user.email:

                # Sending email
                mail_values = {
                    'subject': 'Request for Approval - Yourself',
                    'body_html': """<p>You have received a request for approval of a training plan. Click <a href='http://localhost:8069'>here</a> to log in and access the request.</p>""",
                    'email_to':  selected_user.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()

            else:
                # Handle case where selected user does not have an email
                pass
        else:
            # Handle case where no users are in the group
            pass

    @api.model
    def create(self, vals):
        current_year_month = datetime.now().strftime('%Y%m')
        sequence_code = self.env['ir.sequence'].next_by_code('training.plan') or _('Invalid')
        vals['reference'] = f"{current_year_month}-{sequence_code}"
        res = super(TrainingPlan, self).create(vals)
        return res


class TrainingPlanLines(models.Model):
    _name = "training.plan.lines"
    _description = "training plan lines"
    employee_id = fields.Many2one('hr.employee', string="Candidate Name", required=True, store=True)
    priorityRanking = fields.Integer(string="Priority Ranking", required=True, store=True)
    priorityArea = fields.Char(string="Priority Area", required=True, store=True)

    name = fields.Char(string="Training Proposed", required=True, store=True)
    level_of_training_proposed = fields.Char(string="Level of Training Proposed", required=True, store=True)
    location_of_programme_proposed = fields.Many2one("res.country", "Location of Programme Proposed", required=True,
                                                     store=True)
    proposed_date_of_programme = fields.Date(string="Proposed Date of Programme", required=True, store=True)
    sponsor = fields.Many2one('training.sponsor', string="Sponsor", required=True, store=True)
    justification_of_training = fields.Text(string="Justification of Training", required=True, store=True)
    estimated_cost_per_year = fields.Integer(string="Estimated Cost per Year", required=True, store=True)
    training_plan_id = fields.Many2one('training.plan', string="Training Plan", required=True, store=True)
