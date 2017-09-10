import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
diabetes = datasets.load_diabetes()
feature = diabetes.data[:, np.newaxis, 2]
print(len(feature))
training_data = feature[:-57]
print (len(training_data))
testing_data = feature[-57:]
print(len(testing_data))
output_training = diabetes.target[:-57]
output_testing = diabetes.target[-57:]
regr = linear_model.LinearRegression()
regr.fit(training_data, output_training)
print('Coefficients:', regr.coef_)
print("errors: %.2f"
      % np.mean((regr.predict(testing_data) - output_testing) ** 2))
plt.scatter(testing_data, output_testing,  color='YELLOW')
plt.plot(testing_data, regr.predict(testing_data), color='ORANGE',
         linewidth=5)
plt.xticks(())
plt.yticks(())

plt.show()