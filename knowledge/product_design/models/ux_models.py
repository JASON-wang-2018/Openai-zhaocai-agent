# 产品设计UX模型
# 包含用户体验设计相关模型

class UserPersona:
    def __init__(self, name, age, occupation, goals, pain_points):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.goals = goals
        self.pain_points = pain_points
    
    def get_user_needs(self):
        """获取用户需求"""
        return {
            'primary_needs': self.goals,
            'secondary_needs': self.pain_points
        }

class Wireframe:
    def __init__(self, name, pages):
        self.name = name
        self.pages = pages
    
    def generate_wireframe(self):
        """生成线框图"""
        return {
            'name': self.name,
            'pages': self.pages,
            'structure': self._create_structure()
        }
    
    def _create_structure(self):
        """创建页面结构"""
        structure = {}
        for page in self.pages:
            structure[page] = {
                'elements': ['header', 'navigation', 'content', 'footer'],
                'layout': 'grid'
            }
        return structure

class Prototype:
    def __init__(self, wireframe, interactions):
        self.wireframe = wireframe
        self.interactions = interactions
    
    def create_prototype(self):
        """创建原型"""
        return {
            'wireframe': self.wireframe.generate_wireframe(),
            'interactions': self.interactions,
            'testing_requirements': self._define_testing()
        }
    
    def _define_testing(self):
        """定义测试需求"""
        return {
            'usability_tests': True,
            'a_b_testing': True,
            'user_feedback': True
        }

def conduct_user_research(users):
    """进行用户研究"""
    research_results = []
    for user in users:
        persona = UserPersona(
            user['name'], user['age'], user['occupation'],
            user['goals'], user['pain_points']
        )
        research_results.append(persona.get_user_needs())
    
    return research_results