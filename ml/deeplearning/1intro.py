import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD


# 2D matrix of zeros
a = np.zeros((10, 10))

# Make alternate numbers 1 in a checkerboard format
a[::2, ::2] = 1
a[1::2, 1::2] = 1


# create range and reshape to 10x1
b = np.arange(5, 15).reshape(10, 1)
c = a * b

# mean along axis 0
c.mean(axis=0)


# all c elements where element > 0 and reshape to 10,5
d = c[c>0].reshape(10, 5)

# create gaussian distributed random matrix with mean=0 and std-deviation=0.1
noise = np.random.normal(loc=0.0, scale=0.1, size=(10, 5))

# add noise to another matrix to get another
e = d + noise


# plot matrix with grey colormap - plotted as checkerboard 
plt.imshow(e, cmap='Greys')

# Adding text to plot
plt.xlabel('This is the Xlabel', fontsize=12)
plt.ylabel('This is the Ylabel', fontsize=12)
plt.title('This is the title', fontsize=16)
plt.legend(['S-%s' % i for i in range(e.shape[0])], loc=2);

# Adding annotations to the plot
plt.axvline(1.5, color='orange', linewidth=4)
plt.annotate(
    xy=(1.5, 5.5), xytext=(1.6, 7),   # xy is the point to annotate, xytext is location of text
    text="Very important point",
    arrowprops={"arrowstyle": '-|>'},
    fontsize=12
)

# Given a X and y, plot the decision boundary
def plot_decision_boundary(model, X, y):
    hticks = np.linspace(X.min()-0.1, X.max()+0.1, 101)
    vticks = np.linspace(X.min()-0.1, X.max()+0.1, 101)
    aa, bb = np.meshgrid(hticks, vticks)
    ab = np.c_[aa.ravel(), bb.ravel()]
    c = model.predict(ab)
    cc = c.reshape(aa.shape)
    plt.figure(figsize=(10, 10))
    plt.contourf(aa, bb, cc, cmap='bwr', alpha=0.2)
    plt.plot(X[y==0, 0], X[y==0, 1], 'ob', alpha=0.5)
    plt.plot(X[y==1, 0], X[y==1, 1], 'xr', alpha=0.5)
    plt.title("Blue circles and Red crosses");


# Generating random sample sets
from sklearn.datasets import make_circles
from sklearn.datasets import make_blobs, make_moons

X, y = make_circles(
    n_samples=1000,
    noise=0.1,
    factor=0.2,
    random_state=0
)

Ax, Ay = make_blobs(
    n_samples=1000,
    centers=2,       # by default 3
    random_state=0
)
Bx, By = make_moons(n_samples=1000, noise=0.1)


# Plot sample training sets 

def plot(Ax, Ay, title):
    plt.figure(figsize=(10, 10))
    plt.plot(Ax[Ay==0, 0], Ax[Ay==0, 1], 'ob', alpha=0.5)
    plt.plot(Ax[Ay==1, 0], Ax[Ay==1, 1], 'xr', alpha=0.5)
    plt.xlim(Ax.min(), Ax.max())
    plt.ylim(Ax.min(), Ax.max())
    plt.legend(['0', '1'])
    plt.title(title)


# Training and creating a model
def create_model(X, y):
    # Create model
    model = Sequential()
    model.add(Dense(4, input_shape=(2,), activation='tanh'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(
        optimizer=SGD(lr=0.5),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    # Train model
    model.fit(X, y, epochs=20);
    return model
