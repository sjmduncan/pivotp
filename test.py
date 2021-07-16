# Copyright 2021 Stuart Duncan

from pivotp import *
from pprint import pprint

def gen_data(t_s, t_p, noise_fact = 1.0, num_samples = 16, file_path=''):
  '''Generate some noisy data to test the calibration algorithm. If file_path is
     non-empty then the data will be saved to a file as an example of the expected
     format.
  '''
  data = []
  for ns in range(num_samples):
    euler = np.random.random(3) * 2 * np.pi - np.pi
    r = Rotation.from_euler('xyz', euler)
    noise = np.random.standard_normal(3) * noise_fact
    t = t_p - r.as_dcm() @ t_s + noise
    squat = r.as_quat()
    squat[0],squat[3] = squat[3],squat[0]
    data.append(np.concatenate([t, squat]))
  data = np.array(data)
  if not file_path == '':
    np.savetxt(file_path, data, delimiter=',', header='x,y,z,qw,qx,qy,qz')
  return data

def load_data(file_path):
  return np.genfromtxt(file_path,skip_header=1, delimiter=',')


test_file_path = 'dummy-pose-data.csv'
gen = True # Check to see that test_file_path is not '' and that the file exists/contains data

if gen:
  res_gen = calibrate_stylus(gen_data(
    np.array([30, 50, 120]),     # Expected t_stylus
    np.array([800, 780, 1200]),  # Expected t_pivotp
    1.0,                         # Noise scale factor
    512,                         # Number of samples
    test_file_path))
  pprint(res_gen)
else:
  res_file = calibrate_stylus(load_data(test_file_path))
  pprint(res_file)
