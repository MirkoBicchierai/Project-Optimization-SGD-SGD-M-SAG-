class Solver:
    def __init__(self, precision):
        self.precision = precision

    def sgd(self):
        dataset = DataSet("DataSet/cod-rna-mod.csv", ",", 0)

        x = dataset.data_train
        y = dataset.labels_train
        x, y = np.array(x, dtype="float128"), np.array(y, dtype="float128")
        w = np.zeros(dataset.data_train.shape[1], dtype="float128")

        learn_rate = 0.00001
        batch_size = 64  # x.shape[0]

        n_iter = 5
        n_obs = x.shape[0]
        xy = np.c_[x.reshape(n_obs, -1), y.reshape(n_obs, 1)]

        # Initializing the random number generator
        rng = np.random.default_rng()
        learn_rate = np.array(learn_rate)
        loss = 0
        x_plt = []
        y_plt = []
        for ss in tqdm(range(n_iter)):

            rng.shuffle(xy)
            # Performing minibatch moves
            for start in range(0, n_obs, batch_size):
                stop = start + batch_size
                x_batch, y_batch = xy[start:stop, :-1], xy[start:stop, -1:]
                y_batch = np.squeeze(y_batch, axis=1)

                direction = loss_gradient(x_batch, y_batch, w)
                w = w - learn_rate * direction  # armijo_line_search(x_batch, y_batch, w, -grad)

            print("Train loss: " + str(loss_function(x, y, w)))
            x_plt.append(ss)
            y_plt.append(loss_function(x, y, w))
            # loss += calculate_function(x, y, w)
            # if (ss + 1) % 25 == 0:
            #     print("Train loss epoch " + str(ss + 1) + ": " + str(loss / 10))
            #     loss = 0

            if (ss + 1) % 10 == 0:
                acc = testing(dataset, w)
                print("Accuracy epoch " + str(ss + 1) + ": " + str(acc) + "%")