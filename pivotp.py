# Copyright 2021 Stuart Duncan

from scipy.spatial.transform import Rotation
import numpy as np

def calibrate_stylus(data, swap_w = True ):
  '''Pivot calibration for a 3D stylus.

  data is an Nx7 numpy array of the poses in translation-quaternion encoding
  with collumns in tx,ty,tz,qw,qx,qy,qz order. If your quaternions are in
  qx,qy,qz,qw order then set swap_w to False

  Returns the calibration and RMS residual error
  t_stylus: The stylus tip position in the local coordinate space of the tracked object
  t_pivotp: The pivot point that was used during calibration
  residual: RMS residual error

  '''
  t_i = data[:, 0:3]
  q_i = data[:, 3:7]

  if swap_w:
    # from_quat expects xyzw but data is commonly in wxyz order
    # this swaps the first and last components of the quaternion data
    q_i[:, [0, 3]] = q_i[:, [3, 0]]

  # Create arrays which match the dims and shapes expected by linalg.lstsq
  t_i_shaped = np.array(t_i.reshape(-1,1))
  r_i = Rotation.from_quat(q_i)
  r_i_shaped = []
  for r in r_i:
    r_i_shaped.extend(np.concatenate((r.as_dcm(), -np.identity(3)),axis=1))
  r_i_shaped = np.stack(r_i_shaped)

  # Run least-squares, extract the positions
  lstsq     = np.linalg.lstsq(r_i_shaped,-t_i_shaped)
  t_stylus  = lstsq[0][0:3]
  t_pivotp  = lstsq[0][3:6]

  # Calculate the 3D residual RMS error
  residual_vectors = np.array((t_i_shaped + r_i_shaped@lstsq[0]).reshape(len(t_i),3))
  residual_norms   = np.linalg.norm(residual_vectors,axis=1)
  residual_rms     = np.sqrt(np.mean(residual_norms ** 2))

  return {
    't_stylus': t_stylus[:, 0],
    't_pivotp': t_pivotp[:, 0],
    'residual' : residual_rms}
