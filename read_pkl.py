import pickle

with open('/workspace/assets/examples/driving/nearfar.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)
