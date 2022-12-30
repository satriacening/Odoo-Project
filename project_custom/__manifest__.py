{
    'name': 'Project Custom',
    'version': '1.0',
    'category': 'Services/expenses',
    'summary': 'Project expenses',
    'description': 'Custom module Project For Boston Makmur Gemilang',
    'sequence': 1,
    'depends': [
        'analytic',
        'base_setup',
        'mail',
        'portal',
        'rating',
        'resource',
        'web',
        'web_tour',
        'digest',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/view_project_kanban.xml',
        'views/view_task_form2.xml',
        'views/view_task_kanban.xml',
        'views/view_task_tree2.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}