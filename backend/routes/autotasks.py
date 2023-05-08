from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

import numpy as np
from project_helper import project_exist, user_admin_project






# tags are just for the ui
app = APIRouter(tags=['autotasks'])

class TaskSkills(BaseModel):
    task_skills : dict[int,int]


class Topsis():

    def __init__(self, evaluation_matrix, weight_matrix, criteria):
        # M×N matrix
        self.evaluation_matrix = np.array(evaluation_matrix, dtype="float")

        # M alternatives (options)
        self.row_size = len(self.evaluation_matrix)

        # N attributes/criteria
        self.column_size = len(self.evaluation_matrix[0])

        # N size weight matrix
        self.weight_matrix = np.array(weight_matrix, dtype="float")
        self.weight_matrix = self.weight_matrix / sum(self.weight_matrix)
        self.criteria = np.array(criteria, dtype="float")

    '''
	# Step 2
	The matrix {\displaystyle (x_{ij})_{m\times n}}(x_{{ij}})_{{m\times n}} is then normalised to form the matrix
	'''

    def step_2(self):
        # normalized scores
        self.normalized_decision = np.copy(self.evaluation_matrix)
        sqrd_sum = np.zeros(self.column_size)
        for i in range(self.row_size):
            for j in range(self.column_size):
                sqrd_sum[j] += self.evaluation_matrix[i, j]**2
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.normalized_decision[i,j] = self.evaluation_matrix[i, j]/(sqrd_sum[j]**0.5)

    '''
	# Step 3
	Calculate the weighted normalised decision matrix
	'''

    def step_3(self):
        self.weighted_normalized = np.copy(self.normalized_decision)
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.weighted_normalized[i, j] *= self.weight_matrix[j]

    '''
	# Step 4
	Determine the worst alternative {\displaystyle (A_{w})}(A_{w}) and the best alternative {\displaystyle (A_{b})}(A_{b}):
	'''

    def step_4(self):
        self.worst_alternatives = np.zeros(self.column_size)
        self.best_alternatives = np.zeros(self.column_size)
        for i in range(self.column_size):
            if self.criteria[i]:
                self.worst_alternatives[i] = min(self.weighted_normalized[:, i])
                self.best_alternatives[i] = max(self.weighted_normalized[:, i])
            else:
                self.worst_alternatives[i] = max(self.weighted_normalized[:, i])
                self.best_alternatives[i] = min(self.weighted_normalized[:, i])

    '''
	# Step 5
	Calculate the L2-distance between the target alternative {\displaystyle i}i and the worst condition {\displaystyle A_{w}}A_{w}
	{\displaystyle d_{iw}={\sqrt {\sum _{j=1}^{n}(t_{ij}-t_{wj})^{2}}},\quad i=1,2,\ldots ,m,}
	and the distance between the alternative {\displaystyle i}i and the best condition {\displaystyle A_{b}}A_b
	{\displaystyle d_{ib}={\sqrt {\sum _{j=1}^{n}(t_{ij}-t_{bj})^{2}}},\quad i=1,2,\ldots ,m}
	where {\displaystyle d_{iw}}d_{{iw}} and {\displaystyle d_{ib}}d_{{ib}} are L2-norm distances 
	from the target alternative {\displaystyle i}i to the worst and best conditions, respectively.
	'''

    def step_5(self):
        self.worst_distance = np.zeros(self.row_size)
        self.best_distance = np.zeros(self.row_size)

        self.worst_distance_mat = np.copy(self.weighted_normalized)
        self.best_distance_mat = np.copy(self.weighted_normalized)

        for i in range(self.row_size):
            for j in range(self.column_size):
                self.worst_distance_mat[i][j] = (self.weighted_normalized[i][j]-self.worst_alternatives[j])**2
                self.best_distance_mat[i][j] = (self.weighted_normalized[i][j]-self.best_alternatives[j])**2
                
                self.worst_distance[i] += self.worst_distance_mat[i][j]
                self.best_distance[i] += self.best_distance_mat[i][j]

        for i in range(self.row_size):
            self.worst_distance[i] = self.worst_distance[i]**0.5
            self.best_distance[i] = self.best_distance[i]**0.5

    '''
	# Step 6
	Calculate the similarity
	'''

    def step_6(self):
        np.seterr(all='ignore')
        self.worst_similarity = np.zeros(self.row_size)
        self.best_similarity = np.zeros(self.row_size)

        for i in range(self.row_size):
            # calculate the similarity to the worst condition
            self.worst_similarity[i] = self.worst_distance[i] / \
                (self.worst_distance[i]+self.best_distance[i])

            # calculate the similarity to the best condition
            self.best_similarity[i] = self.best_distance[i] / \
                (self.worst_distance[i]+self.best_distance[i])
    
    def ranking(self, data):
        return [i+1 for i in data.argsort()]

    def rank_to_worst_similarity(self):
        # return rankdata(self.worst_similarity, method="min").astype(int)
        return self.ranking(self.worst_similarity)

    def rank_to_best_similarity(self):
        # return rankdata(self.best_similarity, method='min').astype(int)
        return self.ranking(self.best_similarity)

    def calc(self):
        print("Step 1\n", self.evaluation_matrix, end="\n\n")
        self.step_2()
        print("Step 2\n", self.normalized_decision, end="\n\n")
        self.step_3()
        print("Step 3\n", self.weighted_normalized, end="\n\n")
        self.step_4()
        print("Step 4\n", self.worst_alternatives,
              self.best_alternatives, end="\n\n")
        self.step_5()
        print("Step 5\n", self.worst_distance, self.best_distance, end="\n\n")
        self.step_6()
        print("Step 6\n", self.worst_similarity, self.best_similarity, end="\n\n")



def get_weights(task: TaskSkills):
    weights = []
    sum_weights = sum(task.task_skills.values())

    for  element in task.task_skills.values():
        weights.append(element / sum_weights)

    return weights


def get_criterias_preference_to_maximise(task: TaskSkills):
    l = [True]
    l = l * len(task.task_skills)
    return np.array(l) 
    #return np.array(l + [False])


def get_evaluation_matrix(task: TaskSkills, users):

    #get the list of the skills 
    skills  = list(task.task_skills.keys())

    print("skills", skills)
    print(len(skills))

    # this generates %s,%s,%s, ... depending on the len of array
    format_strings = ','.join(['%s'] * len(skills))

    # this returns {"technology_id": 3 , "technology_id": 14, ...}
    #tech_ids = runSQL("""SELECT technology_id FROM technologies WHERE technology_name IN (""" + format_strings + ")", tuple(skills))

    #get the list of the skills 
    query_pars = list(task.task_skills.keys())
    tech_ids = list(task.task_skills.keys())
    # make list 

    matrix = []
    for user in users:

        matrix_line = runSQL("""SELECT technology_experience FROM users_technologies WHERE user_id = %s AND technology_id IN (""" + format_strings + ")", tuple([user["user_id"]] + query_pars))
        print("m", matrix_line)
        matrix.append(list(matrix_line[0].values()))

    evaluation_matrix = np.array(matrix)
    #print(evaluation_matrix)
    return evaluation_matrix









@app.post("/projects/{project_id}/recommand_user", status_code = status.HTTP_201_CREATED)
def create_task(project_id: int, task: TaskSkills, user_id : int = Depends(get_current_user)):
    # for admins only

    #project_exist(project_id)
    #user_admin_project(project_id, user_id)

    sql ="""SELECT 
            u.user_id,
            m.member_id,
            m.member_role,
            u.username,
            u.img_url
            FROM members m
            LEFT JOIN users u ON m.user_id = u.user_id
            WHERE project_id = %s
        """
    #data = (project_id,)

    users = runSQL(sql,(project_id,))

    if(not users):
        return "no users in project"

    if(len(task.task_skills) == 0):
        return users[0]

    evaluation_matrix = get_evaluation_matrix(task, users)

    weights = get_weights(task)

    criterias = get_criterias_preference_to_maximise(task)


    t = Topsis(evaluation_matrix, weights, criterias)

    t.calc()


    print("best_similarity\t", t.best_similarity)
    print("rank_to_best_similarity\t", t.rank_to_best_similarity())

    #update_project_progress(project_id)

    index = max(t.rank_to_best_similarity()) - 1

    print(users[index])

    return users[index]
    
