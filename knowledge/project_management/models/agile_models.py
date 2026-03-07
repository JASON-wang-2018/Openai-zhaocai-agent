# 项目管理敏捷模型
# 包含敏捷开发相关模型和工具

class Project:
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = []
        self.team_members = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def assign_task(self, task, member):
        task.assignee = member
        member.tasks.append(task)
    
    def calculate_progress(self):
        """计算项目进度"""
        if not self.tasks:
            return 0
        
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        return (completed_tasks / len(self.tasks)) * 100

class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority
        self.completed = False
        self.assignee = None
    
    def mark_completed(self):
        self.completed = True

class TeamMember:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.tasks = []
    
    def get_workload(self):
        """获取工作负载"""
        return len(self.tasks)

def create_sprint_plan(project, duration_days):
    """创建冲刺计划"""
    sprint_tasks = []
    for task in project.tasks:
        if task.priority in ['high', 'medium']:
            sprint_tasks.append(task)
    
    return {
        'sprint_duration': duration_days,
        'tasks': sprint_tasks,
        'team_members': project.team_members
    }