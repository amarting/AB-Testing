
"""
The bayesian_test function is based on a post by Evan Miller.
More at http://www.evanmiller.org/bayesian-ab-testing.html
The bayesian_function_update is explained in my blog,
https://salasboni.wordpress.com/2015/02/06/online-formula-bayesian-ab-testing/
Author: Rebeca Salas-Boni
Email: salasboni@gmail.com
"""
def generate_one_experiment(total_number_of_visitors, prob_of_showing_version_A, p_A_true, p_B_true):

    size_A = 0
    num_conversions_A = 0
    size_B = 0
    num_conversions_B = 0
    probs_bayesian = [0]*total_number_of_visitors
    probs_bayesian_online = [0]*total_number_of_visitors

    probs_bayesian_online[0] = 0.5

    for j in range(1, total_number_of_visitors):

        visitor = int(random() < prob_of_showing_version_A)

        if visitor:
            size_A += 1
            visitor_converts = int(random() < p_A_true)
            num_conversions_A += visitor_converts
            if visitor_converts:
                changing_variable = 'alpha_A'
            else:
                changing_variable = 'beta_A'
        else:
            size_B += 1
            visitor_converts = int(random() < p_B_true)
            num_conversions_B += visitor_converts
            if visitor_converts:
                changing_variable = 'alpha_B'
            else:
                changing_variable = 'beta_B'

        alpha_A = num_conversions_A + 1
        beta_A = size_A - num_conversions_A + 1
        alpha_B = num_conversions_B + 1
        beta_B = size_B - num_conversions_B + 1

        prob_pB_greater_than_pA_old = probs_bayesian_online[j-1]

        prob_pB_greater_than_pA_bayesian = bayesian_test(alpha_A, beta_A, alpha_B, beta_B)
        prob_pB_greater_than_pA_bayesian_online = bayesian_test_online(alpha_A, beta_A,
              alpha_B, beta_B, prob_pB_greater_than_pA_old, changing_variable)

        probs_bayesian[j] = prob_pB_greater_than_pA_bayesian
        probs_bayesian_online[j] = prob_pB_greater_than_pA_bayesian_online

    return probs_bayesian, probs_bayesian_online


def bayesian_test(alpha_A, beta_A, alpha_B, beta_B):

    prob_pB_greater_than_pA = 0
    for i in range(0, alpha_B):
        prob_pB_greater_than_pA += exp(log(beta(alpha_A + i, beta_B + beta_A)) - log(beta_B + i) -
                                       log(beta(1 + i, beta_B)) - log(beta(alpha_A, beta_A)))

    return prob_pB_greater_than_pA


def bayesian_test_online(alpha_A, beta_A, alpha_B, beta_B, prob_pB_greater_than_pA_old, changing_variable):

    if changing_variable =='alpha_A':
        prob_pB_greater_than_pA = prob_pB_greater_than_pA_old - exp(log(beta(alpha_B + alpha_A - 1, beta_B + beta_A))
                        - log(beta_A + alpha_A - 1) - log(beta(alpha_A, beta_A)) - log(beta(alpha_B, beta_B)))
    if changing_variable =='alpha_B':
        prob_pB_greater_than_pA = prob_pB_greater_than_pA_old + exp(log(beta(alpha_A + alpha_B - 1, beta_B + beta_A))
                        - log(beta_B + alpha_B - 1) - log(beta(alpha_B, beta_B)) - log(beta(alpha_A, beta_A)))
    if changing_variable =='beta_A':
        prob_pB_greater_than_pA = prob_pB_greater_than_pA_old + exp(log(beta(beta_B + beta_A - 1, alpha_B + alpha_A))
                        - log(alpha_A + beta_A - 1) - log(beta(beta_A, alpha_A)) - log(beta(alpha_B, beta_B)))
    if changing_variable =='beta_B':
        prob_pB_greater_than_pA = prob_pB_greater_than_pA_old - exp(log(beta(beta_A + beta_B - 1, alpha_B + alpha_A))
                        - log(alpha_B + beta_B - 1) - log(beta(beta_B, alpha_B)) - log(beta(alpha_A, beta_A)))

    return prob_pB_greater_than_pA


from scipy.special import beta
import matplotlib.pyplot as plt
from math import log, exp
from random import random

total_number_of_visitors = 1000
p_A_true = .2
p_B_true = .3
prob_of_showing_version_A = .5

probs_bayesian, probs_bayesian_online = generate_one_experiment(total_number_of_visitors,
                prob_of_showing_version_A, p_A_true, p_B_true)


plt.figure()

plt.subplot(211)
plt.plot(probs_bayesian)
plt.title('Bayesian A/B testing')
plt.ylabel('Prob(pA < pB)')
plt.ylim([0, 1])

plt.subplot(212)
plt.plot(probs_bayesian_online, color='red')
plt.title('Online Bayesian A/B testing')
plt.xlabel('Visitor number')
plt.ylabel('Prob(pA < pB)')
plt.ylim([0, 1])

plt.show()

