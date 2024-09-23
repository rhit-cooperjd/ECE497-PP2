import matplotlib.pyplot as plt
import numpy as np
import dystopia_ea as ea
from scipy.stats import poisson

rebel_list = []
soldier_list = []

def populate_rebels(population_size, charisma, strength):
    global rebel_list
    for rebel in range(population_size):
        rebel = ea.Fighter(strength, charisma)
        rebel.rebel_run()
        rebel_list.append(rebel)

def populate_soldiers(population_size, charisma, strength):
    global soldier_list
    for soldier in range(population_size):
        soldier = ea.Fighter(strength, charisma)
        soldier.soldier_run()
        soldier_list.append(soldier)
    
def train_rebels(charisma_threshold):
    global rebel_list
    rebel_1_index = np.random.randint(0, len(rebel_list))
    rebel_2_index = np.random.randint(0, len(rebel_list))
    while rebel_2_index == rebel_1_index:
        rebel_2_index = np.random.randint(0, len(rebel_list))
    if rebel_list[rebel_1_index].charisma > charisma_threshold and rebel_list[rebel_2_index].charisma > charisma_threshold:
        sum_charisma = rebel_list[rebel_1_index].charisma + rebel_list[rebel_2_index].charisma
        avg_strength = (rebel_list[rebel_1_index].strength + rebel_list[rebel_2_index].strength)/2
        rebel_list[rebel_1_index].charisma = sum_charisma
        rebel_list[rebel_2_index].strength = avg_strength

def average_traits(fighter_list):
    charisma_list = []
    strength_list = []
    for i in range(len(fighter_list)):
        charisma_list.append(fighter_list[i].charisma)
        strength_list.append(fighter_list[i].strength)
    return np.average(charisma_list), np.average(strength_list)    

def visualize_rebels_training(population_size, charisma, strength, duration, charisma_threshold):
    global rebel_list
    avg_charisma = 0
    avg_strength = 0

    populate_rebels(population_size, charisma, strength)
    
    avg_charisma, avg_strength = average_traits(rebel_list)
    
    fig, ax = plt.subplots(2, 1)
    before_bar_container = ax[0].bar(['Charisma', 'Strength'], [avg_charisma, avg_strength])
    ax[0].set_ylabel('Trait Score')
    ax[0].set_title('Rebel Traits Before Training')
    ax[0].bar_label(before_bar_container)
    
    while duration > 0:
        train_rebels(charisma_threshold)
        duration = duration - 1

    avg_charisma, avg_strength = average_traits(rebel_list)
    
    after_bar_container = ax[1].bar(['Charisma', 'Strength'], [avg_charisma, avg_strength])
    ax[1].set_ylabel('Trait Score')
    ax[1].set_title('Rebel Traits After Training')
    ax[1].bar_label(after_bar_container)
    plt.show()

def dystopia_sim(rebel_population_size, rebel_base_charisma, rebel_base_strength, soldier_population_size, soldier_base_charisma, soldier_base_strength, duration, charisma_threshold):
    global rebel_list
    global soldier_list
    global k
    avg_charisma = 0
    avg_strength = 0
    initial_avg_soldier_charisma = 0
    initial_avg_soldier_strength = 0

    populate_rebels(rebel_population_size, rebel_base_charisma, rebel_base_strength)
    populate_soldiers(soldier_population_size, soldier_base_charisma, soldier_base_strength)
    
    fig, ax = plt.subplots(2, 2)

    avg_charisma, avg_strength = average_traits(rebel_list)
    rebel_before_bar_container = ax[0][0].bar(['Charisma', 'Strength'], [avg_charisma, avg_strength])
    ax[0][0].set_ylabel('Trait Score')
    ax[0][0].set_title('Rebel Traits Before Training')
    ax[0][0].bar_label(rebel_before_bar_container)

    initial_avg_soldier_charisma, initial_avg_soldier_strength = average_traits(soldier_list)
    
    while duration > 0:
        if check_for_winner() == False:
            train_rebels(charisma_threshold)
            contest(charisma_threshold)
            duration = duration - 1
        else:
            break

    avg_charisma, avg_strength = average_traits(soldier_list)

    soldier_average_bar_labels = ['Initial Charisma', 'Initial Strength', 'Final Charisma', 'Final Strength']
    y_pos = np.arange(len(soldier_average_bar_labels))
    ax[0][1].barh(y_pos, [initial_avg_soldier_charisma, initial_avg_soldier_strength, avg_charisma, avg_strength], align='center')
    ax[0][1].set_yticks(y_pos, labels=soldier_average_bar_labels)
    ax[0][1].invert_yaxis()
    ax[0][1].set_xlabel('Average Trait Values')
    ax[0][1].set_title('Average Soldier Trait Values')
        
    avg_charisma, avg_strength = average_traits(rebel_list)
    
    rebel_after_bar_container = ax[1][0].bar(['Charisma', 'Strength'], [avg_charisma, avg_strength])
    ax[1][0].set_ylabel('Trait Score')
    ax[1][0].set_title('Rebel Traits After Training')
    ax[1][0].bar_label(rebel_after_bar_container)

    population_change_bar_container = ax[1][1].bar(['Initial # Rebels', 'Initial # Soldiers', 'Final # Rebels', 'Final # Soldiers'],
                                                   [rebel_population_size, soldier_population_size, len(rebel_list), len(soldier_list)])
    ax[1][1].set_ylabel('Population')
    ax[1][1].set_title('Changes in Population')
    ax[1][1].bar_label(population_change_bar_container)

    plt.show()
    print(len(soldier_list))
    print(len(rebel_list))
    check_for_winner()

def defect(soldier): 
    global soldier_list 
    global rebel_list
    mu = 0.10*len(soldier_list) # out of 100 soldiers, on average, 10 will defect per conflict
    if poisson.pmf(1, mu) > 0.10:
        soldier_list.remove(soldier)
        rebel_list.append(soldier)

def visualize_defection(population_size, charisma, strength, duration, charisma_threshold):
    populate_rebels(population_size, charisma, strength)
    populate_soldiers(population_size, charisma, strength)
    while duration > 0:
        if check_for_winner() == False:
            train_rebels(charisma_threshold)
            contest(charisma_threshold)
            duration = duration - 1
        else:
            break
    bar_container = plt.bar(['Initial Army', 'After Defection'], [population_size, len(soldier_list)])
    plt.bar_label(bar_container)
    plt.ylabel('Population')
    plt.title('Change in Soldier Numbers Due to Defection')
    plt.show()  

def contest(charisma_threshold):
    global rebel_list
    global soldier_list
    rebel = rebel_list[np.random.randint(len(rebel_list))]
    soldier = soldier_list[np.random.randint(len(soldier_list))]
    if rebel.charisma > soldier.charisma + charisma_threshold:
        defect(soldier)
    else:
        if rebel.strength <= soldier.strength:
            rebel_list.remove(rebel)
        else:
            soldier_list.remove(soldier)

def check_for_winner():
    global rebel_list
    global soldier_list
    if len(rebel_list) == 0:
        print("THE DOMINION WILL NEVER FALL! The rebellion is squashed!")
        return True
    elif len(soldier_list) == 0:
        print("REVOLT! The Dominion has fallen! The rebels win!")
        return True
    else:
        print("THE STRUGGLE IS ETERNAL!\nRebel numbers: {}\nSoldier numbers: {}".format(len(rebel_list), len(soldier_list)))
        return False

# THE STRUGGLE BEGINS: The evil dystopian government, The Dominion, is oppressing the people of the Land of Attena. Brave rebels fight for freedom, but
# will their efforts be in vain?
duration = 1000

# SCENARIO 1: # soldiers = # rebels, base values the same
# rebel_population_size = 1000
# rebel_base_charisma = 0
# rebel_base_strength = 0
# charisma_threshold = 1
# soldier_population_size = 1000
# soldier_base_charisma = 0
# soldier_base_strength = 0

# # SCENARIO 2: # soldiers > # rebels, base values the same
# rebel_population_size = 500
# rebel_base_charisma = 0
# rebel_base_strength = 0
# charisma_threshold = 1
# soldier_population_size = 1000
# soldier_base_charisma = 0
# soldier_base_strength = 0

# # SCENARIO 3: # soldiers < # rebels, base values the same
# rebel_population_size = 1000
# rebel_base_charisma = 0
# rebel_base_strength = 0
# charisma_threshold = 1
# soldier_population_size = 500
# soldier_base_charisma = 0
# soldier_base_strength = 0

# # SCENARIO 4: # soldiers = # rebels, soldier base charisma > rebel base charisma
# rebel_population_size = 1000
# rebel_base_charisma = 0
# rebel_base_strength = 0
# charisma_threshold = 1
# soldier_population_size = 1000
# soldier_base_charisma = 2
# soldier_base_strength = 0

# # SCENARIO 5: # soldiers = # rebels, soldier base charisma < rebel base charisma
rebel_population_size = 1000
rebel_base_charisma = 2
rebel_base_strength = 0
charisma_threshold = 1
soldier_population_size = 1000
soldier_base_charisma = 0
soldier_base_strength = 0

# Phase 1
# Implement the algorithm for rebel reproduction and graph trends of changing traits
# visualize_rebels_training(rebel_population_size, rebel_base_charisma, rebel_base_strength, duration, charisma_threshold)

# Phase 2
# Implement soldier conversion and graph
# visualize_defection(rebel_population_size, rebel_base_charisma, rebel_base_strength, duration, charisma_threshold)

# Phase 3
# Implement full simulation: will the Dominion finally fall?
dystopia_sim(rebel_population_size, rebel_base_charisma, rebel_base_strength, soldier_population_size, soldier_base_charisma, soldier_base_strength,
             duration, charisma_threshold)




    