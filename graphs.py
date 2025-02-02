import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np

# Load the MATLAB file
data = sio.loadmat('./mydata.mat')
data_subs = data['data_subs'][0, 0]

# Extract subject IDs (flattened array of strings)
subject_ids = np.array([str(subject[0][0]) for subject in data_subs['subjectID'][0]])
print("Subject IDs:", subject_ids)

# Extract scenarios and ensure they are numpy arrays
scen1 = np.array(data_subs['Scen1'])
scen2 = np.array(data_subs['Scen2'])
scen3 = np.array(data_subs['Scen3'])
scen4 = np.array(data_subs['Scen4'])
scen5 = np.array(data_subs['Scen5'])

# Assuming 'ScenX' fields are numpy arrays of shape (subjects, conditions)
scenarios = [scen1, scen2, scen3, scen4, scen5]
titles = ['Ambient', 'Drum Beat', 'Instrumental', 'Piano', 'Poetry']
conditions = ['Dry Sound', 'Opera Hall', 'Reverb Hall', 'Small Office']

# Plotting
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, (scenario, title) in enumerate(zip(scenarios, titles)):
    ax = axes[i]
    for j, condition in enumerate(conditions):
        try:
            y_values = scenario[:, j]  # Extract the column for the condition
        except IndexError as e:
            print(f"IndexError for scenario {title}, condition {condition}: {e}")
            continue
        except Exception as e:
            print(f"Error for scenario {title}, condition {condition}: {e}")
            continue

        # Check if dimensions match
        if len(subject_ids) != 1:
            print(f"Dimension mismatch for scenario {title}, condition {condition}: x ({len(subject_ids)}) vs y ({len(y_values)})")
            continue

        # Plotting
        ax.plot(range(len(y_values)), y_values, label=condition)
    ax.set_title(title)
    ax.set_xlabel('Subject ID')
    ax.set_ylabel('Score')
    ax.legend()

# Hide the last subplot (since we only need 5)
axes[-1].axis('off')

plt.tight_layout()
plt.show()
