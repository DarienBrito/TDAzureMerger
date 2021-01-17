# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2018 www.open3d.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------

import open3d as o3d
import numpy as np

if o3d.__DEVICE_API__ == 'cuda':
    from open3d.cuda.pybind.core import (Dtype, DtypeCode, Device, cuda, nns,
                                         NoneType, TensorList, SizeVector,
                                         matmul as pybind_matmul, lstsq as
                                         pybind_lstsq, solve as pybind_solve,
                                         inv as pybind_inv, svd as pybind_svd)
else:
    from open3d.cpu.pybind.core import (Dtype, DtypeCode, Device, cuda, nns,
                                        NoneType, TensorList, SizeVector, matmul
                                        as pybind_matmul, lstsq as pybind_lstsq,
                                        solve as pybind_solve, inv as
                                        pybind_inv, svd as pybind_svd)

none = NoneType()


def _numpy_dtype_to_dtype(numpy_dtype):
    if numpy_dtype == np.float32:
        return Dtype.Float32
    elif numpy_dtype == np.float64:
        return Dtype.Float64
    elif numpy_dtype == np.int32:
        return Dtype.Int32
    elif numpy_dtype == np.int64:
        return Dtype.Int64
    elif numpy_dtype == np.uint8:
        return Dtype.UInt8
    elif numpy_dtype == np.uint16:
        return Dtype.UInt16
    elif numpy_dtype == np.bool:
        return Dtype.Bool
    else:
        raise ValueError("Unsupported numpy dtype:", numpy_dtype)


def cast_to_py_tensor(func):
    """
    Args:
        func: function returning a `o3d.pybind.core.Tensor`.

    Return:
        A function which returns a python object `Tensor`.
    """

    def _maybe_to_py_tensor(c_tensor):
        if isinstance(c_tensor, o3d.pybind.core.Tensor):
            py_tensor = Tensor([])
            py_tensor.shallow_copy_from(c_tensor)
            return py_tensor
        else:
            return c_tensor

    def wrapped_func(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if isinstance(result, list):
            return [_maybe_to_py_tensor(val) for val in result]
        elif isinstance(result, tuple):
            return tuple([_maybe_to_py_tensor(val) for val in result])
        else:
            return _maybe_to_py_tensor(result)

    return wrapped_func


def _to_o3d_tensor_key(key):

    if isinstance(key, int):
        return o3d.pybind.core.TensorKey.index(key)
    elif isinstance(key, slice):
        return o3d.pybind.core.TensorKey.slice(
            none if key.start == None else key.start,
            none if key.stop == None else key.stop,
            none if key.step == None else key.step)
    elif isinstance(key, (tuple, list)):
        key = np.array(key).astype(np.int64)
        return o3d.pybind.core.TensorKey.index_tensor(Tensor(key))
    elif isinstance(key, np.ndarray):
        key = key.astype(np.int64)
        return o3d.pybind.core.TensorKey.index_tensor(Tensor(key))
    elif isinstance(key, Tensor):
        return o3d.pybind.core.TensorKey.index_tensor(key)
    else:
        raise TypeError("Invalid key type {}.".format(type(key)))


@cast_to_py_tensor
def matmul(lhs, rhs):
    """
    Matrix multiplication between Tensor \param lhs and Tensor \param rhs

    Args:
      lhs: Tensor of shape (m, k)
      rhs: Tensor of shape (k, n)

    Returns:
      Tensor of shape (m, n)

    - Both tensors should share the same device and dtype.
    - Int32, Int64, Float32, Float64 are supported,
      but results of big integers' matmul are not guaranteed, overflow can
      happen.
    """
    return pybind_matmul(lhs, rhs)


@cast_to_py_tensor
def solve(lhs, rhs):
    """
    Returns X by solving linear system AX = B with LU decomposition,
    where A is Tensor \param lhs and B is Tensor \param rhs.

    Args:
      lhs: Tensor of shape (n, n)
      rhs: Tensor of shape (n, k)

    Returns:
      Tensor of shape (n, k)

    - Both tensors should share the same device and dtype.
    - Float32 and Float64 are supported.
    """
    return pybind_solve(lhs, rhs)


@cast_to_py_tensor
def lstsq(lhs, rhs):
    """
    Returns X by solving linear system AX = B with QR decomposition,
    where A is Tensor \param lhs and B is Tensor \param rhs.

    Args:
      lhs: Tensor of shape (m, n), m >= n and is a full rank matrix.
      rhs: Tensor of shape (m, k)

    Returns:
      Tensor of shape (n, k)

    - Both tensors should share the same device and dtype.
    - Float32 and Float64 are supported.
    """
    return pybind_lstsq(lhs, rhs)


@cast_to_py_tensor
def inv(val):
    """
    Returns matrix's inversion with LU decomposition.

    Args:
      val: Tensor of shape (m, m) and is an invertable matrix

    Returns:
      Tensor of shape (m, m)

    - Float32 and Float64 are supported.
    """
    return pybind_inv(val)


@cast_to_py_tensor
def svd(val):
    """
    Returns matrix's SVD decomposition: U S VT = A, where A is Tensor \param val.

    Args:
      val: Tensor of shape (m, n).

    Returns: a tuple of tensors:
      U: Tensor of shape (m, n)
      S: Tensor of shape (min(m, n))
      VT: Tensor of shape (n, n)

    - Float32 and Float64 are supported.
    """
    return pybind_svd(val)


class Tensor(o3d.pybind.core.Tensor):
    """
    Open3D Tensor class. A Tensor is a view of data blob with shape, strides
    and etc. Tensor can be used to perform numerical operations.
    """

    def __init__(self, data, dtype=None, device=None):
        if isinstance(data, (tuple, list, int, float)):
            data = np.array(data)
        if not isinstance(data, np.ndarray):
            raise ValueError("data must be a list, tuple, or Numpy array.")
        if dtype is None:
            dtype = _numpy_dtype_to_dtype(data.dtype)
        if device is None:
            device = Device("CPU:0")
        super(Tensor, self).__init__(data, dtype, device)

    @cast_to_py_tensor
    def __getitem__(self, key):
        t = self
        if isinstance(key, tuple):
            o3d_tensor_keys = [_to_o3d_tensor_key(k) for k in key]
            t = super(Tensor, self)._getitem_vector(o3d_tensor_keys)
        elif isinstance(key, (int, slice, list, np.ndarray, Tensor)):
            t = super(Tensor, self)._getitem(_to_o3d_tensor_key(key))
        else:
            raise TypeError("Invalid type {} for getitem.".format(type(key)))
        return t

    @cast_to_py_tensor
    def __setitem__(self, key, value):
        if not isinstance(value, Tensor):
            value = Tensor(value, self.dtype, self.device)
        if isinstance(key, tuple):
            o3d_tensor_keys = [_to_o3d_tensor_key(k) for k in key]
            super(Tensor, self)._setitem_vector(o3d_tensor_keys, value)
        elif isinstance(key, (int, slice, list, np.ndarray, Tensor)):
            super(Tensor, self)._setitem(_to_o3d_tensor_key(key), value)
        else:
            raise TypeError("Invalid type {} for getitem.".format(type(key)))
        return self

    @staticmethod
    @cast_to_py_tensor
    def empty(shape, dtype, device=Device("CPU:0")):
        """
        Create a tensor with uninitilized values.

        Args:
            shape (list, tuple, SizeVector): Shape of the tensor.
            dtype (Dtype): Data type of the tensor.
            device (Device): Device where the tensor is created.
        """
        if not isinstance(shape, SizeVector):
            shape = SizeVector(shape)
        return super(Tensor, Tensor).empty(shape, dtype, device)

    @staticmethod
    @cast_to_py_tensor
    def full(shape, fill_value, dtype, device=Device("CPU:0")):
        """
        Create a tensor with fill with the specified value.

        Args:
            shape (list, tuple, SizeVector): Shape of the tensor.
            fill_value (scalar): The value to be filled.
            dtype (Dtype): Data type of the tensor.
            device (Device): Device where the tensor is created.
        """
        if not isinstance(shape, SizeVector):
            shape = SizeVector(shape)
        return super(Tensor, Tensor).full(shape, fill_value, dtype, device)

    @staticmethod
    @cast_to_py_tensor
    def zeros(shape, dtype, device=Device("CPU:0")):
        """
        Create a tensor with fill with zeros.

        Args:
            shape (list, tuple, SizeVector): Shape of the tensor.
            dtype (Dtype): Data type of the tensor.
            device (Device): Device where the tensor is created.
        """
        if not isinstance(shape, SizeVector):
            shape = SizeVector(shape)
        return super(Tensor, Tensor).zeros(shape, dtype, device)

    @staticmethod
    @cast_to_py_tensor
    def ones(shape, dtype, device=Device("CPU:0")):
        """
        Create a tensor with fill with ones.

        Args:
            shape (list, tuple, SizeVector): Shape of the tensor.
            dtype (Dtype): Data type of the tensor.
            device (Device): Device where the tensor is created.
        """
        if not isinstance(shape, SizeVector):
            shape = SizeVector(shape)
        return super(Tensor, Tensor).ones(shape, dtype, device)

    @staticmethod
    @cast_to_py_tensor
    def eye(n, dtype=Dtype.Float64, device=Device("CPU:0")):
        """
        Create an identity square matrix.

        Args:
            n (int): size of square matrix
            dtype (Dtype): Data type of the tensor.
            device (Device): Device where the tensor is created.
        """
        return super(Tensor, Tensor).eye(n, dtype, device)

    @staticmethod
    @cast_to_py_tensor
    def diag(value):
        """
        Create an diagonal square matrix.

        Args:
            value (Tensor): array of numbers on the diagonal
        """
        return super(Tensor, Tensor).diag(value)

    @cast_to_py_tensor
    def cuda(self, device_id=0):
        """
        Returns a copy of this tensor in CUDA memory.

        Args:
            device_id: CUDA device id.
        """
        return super(Tensor, self).cuda(device_id)

    @cast_to_py_tensor
    def cpu(self):
        """
        Returns a copy of this tensor in CPU.

        If the Tensor is already in CPU, then no copy is performed.
        """
        return super(Tensor, self).cpu()

    def numpy(self):
        """
        Returns this tensor as a NumPy array. This tensor must be a CPU tensor,
        and the returned NumPy array shares the same memory as this tensor.
        Changes to the NumPy array will be reflected in the original tensor and
        vice versa.
        """
        return super(Tensor, self).numpy()

    @staticmethod
    @cast_to_py_tensor
    def from_numpy(np_array):
        """
        Returns a Tensor from NumPy array. The resulting tensor is a CPU tensor
        that shares the same memory as the NumPy array. Changes to the tensor
        will be reflected in the original NumPy array and vice versa.

        Args:
            np_array: The Numpy array to be converted from.
        """
        return super(Tensor, Tensor).from_numpy(np_array)

    def to_dlpack(self):
        """
        Returns a DLPack PyCapsule representing this tensor.
        """
        return super(Tensor, self).to_dlpack()

    @staticmethod
    @cast_to_py_tensor
    def from_dlpack(dlpack):
        """
        Returns a tensor converted from DLPack PyCapsule.
        """
        return super(Tensor, Tensor).from_dlpack(dlpack)

    @cast_to_py_tensor
    def add(self, value):
        """
        Adds a tensor and returns the resulting tensor.
        """
        return super(Tensor, self).add(value)

    @cast_to_py_tensor
    def add_(self, value):
        """
        Inplace version of Tensor.add.
        """
        return super(Tensor, self).add_(value)

    @cast_to_py_tensor
    def sub(self, value):
        """
        Substracts a tensor and returns the resulting tensor.
        """
        return super(Tensor, self).sub(value)

    @cast_to_py_tensor
    def sub_(self, value):
        """
        Inplace version of Tensor.sub.
        """
        return super(Tensor, self).sub_(value)

    @cast_to_py_tensor
    def mul(self, value):
        """
        Multiplies a tensor and returns the resulting tensor.
        """
        return super(Tensor, self).mul(value)

    @cast_to_py_tensor
    def mul_(self, value):
        """
        Inplace version of Tensor.mul.
        """
        return super(Tensor, self).mul_(value)

    @cast_to_py_tensor
    def div(self, value):
        """
        Divides a tensor and returns the resulting tensor.
        """
        return super(Tensor, self).div(value)

    @cast_to_py_tensor
    def div_(self, value):
        """
        Inplace version of Tensor.div.
        """
        return super(Tensor, self).div_(value)

    @cast_to_py_tensor
    def abs(self):
        """
        Returns element-wise absolute value of a tensor.
        """
        return super(Tensor, self).abs()

    @cast_to_py_tensor
    def abs_(self):
        """
        Inplace version of Tensor.abs.
        """
        return super(Tensor, self).abs_()

    @cast_to_py_tensor
    def logical_and(self, value):
        """
        Element-wise logical and operation.

        If the tensor is not boolean, zero will be treated as False, while
        non-zero values will be treated as True.
        """
        return super(Tensor, self).logical_and(value)

    @cast_to_py_tensor
    def logical_and_(self, value):
        """
        Inplace version of Tensor.logical_and.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).logical_and_(value)

    @cast_to_py_tensor
    def logical_or(self, value):
        """
        Element-wise logical or operation.

        If the tensor is not boolean, zero will be treated as False, while
        non-zero values will be treated as True.
        """
        return super(Tensor, self).logical_or(value)

    @cast_to_py_tensor
    def logical_or_(self, value):
        """
        Inplace version of Tensor.logical_or.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).logical_or_(value)

    @cast_to_py_tensor
    def logical_xor(self, value):
        """
        Element-wise logical exclusive-or operation.

        If the tensor is not boolean, zero will be treated as False, while
        non-zero values will be treated as True.
        """
        return super(Tensor, self).logical_xor(value)

    @cast_to_py_tensor
    def logical_xor_(self, value):
        """
        Inplace version of Tensor.logical_xor.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).logical_xor_(value)

    @cast_to_py_tensor
    def gt(self, value):
        """
        Element-wise greater than operation, returning a new boolean tensor.
        """
        return super(Tensor, self).gt(value)

    @cast_to_py_tensor
    def gt_(self, value):
        """
        Inplace version of Tensor.gt.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).gt_(value)

    @cast_to_py_tensor
    def lt(self, value):
        """
        Element-wise less than operation, returning a new boolean tensor.
        """
        return super(Tensor, self).lt(value)

    @cast_to_py_tensor
    def lt_(self, value):
        """
        Inplace version of Tensor.lt.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).lt_(value)

    @cast_to_py_tensor
    def ge(self, value):
        """
        Element-wise greater-than-or-equals-to operation, returning a new
        boolean tensor.
        """
        return super(Tensor, self).ge(value)

    @cast_to_py_tensor
    def ge_(self, value):
        """
        Inplace version of Tensor.ge.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).ge_(value)

    @cast_to_py_tensor
    def le(self, value):
        """
        Element-wise less-than-or-equals-to than operation, returning a new
        boolean tensor.
        """
        return super(Tensor, self).le(value)

    @cast_to_py_tensor
    def le_(self, value):
        """
        Inplace version of Tensor.le.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).le_(value)

    @cast_to_py_tensor
    def eq(self, value):
        """
        Element-wise equal operation, returning a new boolean tensor.
        """
        return super(Tensor, self).eq(value)

    @cast_to_py_tensor
    def eq_(self, value):
        """
        Inplace version of Tensor.eq.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).eq_(value)

    @cast_to_py_tensor
    def ne(self, value):
        """
        Element-wise not-equal operation, returning a new boolean tensor.
        """
        return super(Tensor, self).ne(value)

    @cast_to_py_tensor
    def ne_(self, value):
        """
        Inplace version of Tensor.ne.

        This operation won't change the tensor's dtype.
        """
        return super(Tensor, self).ne_(value)

    @cast_to_py_tensor
    def to(self, dtype, copy=False):
        """
        Returns a tensor with the specified dtype.

        Args:
            dtype: The targeted dtype to convert to.
            copy: If true, a new tensor is always created; if false, the copy
                  is avoided when the original tensor already have the targeted
                  dtype.
        """
        return super(Tensor, self).to(dtype, copy)

    @cast_to_py_tensor
    def contiguous(self):
        """
        Returns a contiguous Tensor containing the same data in the same device.
        If self tensor is already contiguous, the same underlying memory will be
        used.
        """
        return super(Tensor, self).contiguous()

    @cast_to_py_tensor
    def T(self):
        """
        Expects input to be <= 2-D Tensor by swapping dimension 0 and 1.
        0-D and 1-D Tensor remains the same.
        """
        return super(Tensor, self).T()

    @cast_to_py_tensor
    def nonzero(self, as_tuple=False):
        if as_tuple:
            return super(Tensor, self)._non_zero_numpy()
        else:
            return super(Tensor, self)._non_zero()

    @cast_to_py_tensor
    def matmul(self, value):
        """
        Matrix multiplication between Tensor \param self and Tensor \param value

        Args:
          self: Tensor of shape (m, k)
          value: Tensor of shape (k, n)

        Returns:
          Tensor of shape (m, n)

        - Both tensors should share the same device and dtype.
        - Int32, Int64, Float32, Float64 are supported,
          but results of big integers' matmul are not guaranteed, overflow can
          happen.
        """
        return super(Tensor, self).matmul(value)

    @cast_to_py_tensor
    def solve(self, value):
        """
        Returns X by solving linear system AX = B with LU decomposition,
        where A is Tensor \param self and B is Tensor \param value.

        Args:
          self: Tensor of shape (n, n)
          value: Tensor of shape (n, k)

        Returns:
          Tensor of shape (n, k)

        - Both tensors should share the same device and dtype.
        - Float32 and Float64 are supported.
        """
        return super(Tensor, self).solve(value)

    @cast_to_py_tensor
    def lstsq(self, value):
        """
        Returns X by solving linear system AX = B with QR decomposition,
        where A is Tensor \param self and B is Tensor \param value.
        Use it only when A is non-square.

        Args:
          self: Tensor of shape (m, n), m >= n and is a full rank matrix.
          value: Tensor of shape (m, k)

        Returns:
          Tensor of shape (n, k)

        - Both tensors should share the same device and dtype.
        - Float32 and Float64 are supported.
        - The result can be unexpected when A is not a full-rank matrix and the
          backend is cuda.
        """
        return super(Tensor, self).lstsq(value)

    @cast_to_py_tensor
    def inv(self):
        """
        Returns matrix's inversion with LU decomposition.

        Args:
          self: Tensor of shape (m, m) and is an invertable matrix

        Returns:
          Tensor of shape (m, m)

        - Float32 and Float64 are supported.
        """
        return super(Tensor, self).inv()

    @cast_to_py_tensor
    def svd(self):
        """
        Returns matrix's SVD decomposition: U S VT = A, where A is Tensor
        \param self.

        Args:
          self: Tensor of shape (m, n).

        Returns: a tuple of tensors:
          U: Tensor of shape (m, n)
          S: Tensor of shape (min(m, n))
          VT: Tensor of shape (n, n)

        - Float32 and Float64 are supported.
        """
        return super(Tensor, self).svd()

    def __add__(self, value):
        return self.add(value)

    def __radd__(self, value):
        return self.add(value)

    def __iadd__(self, value):
        return self.add_(value)

    def __sub__(self, value):
        return self.sub(value)

    def __rsub__(self, value):
        return Tensor.full((), value, self.dtype, self.device) - self

    def __isub__(self, value):
        return self.sub_(value)

    def __mul__(self, value):
        return self.mul(value)

    def __rmul__(self, value):
        return self.mul(value)

    def __matmul__(self, value):
        return self.matmul(value)

    def __imul__(self, value):
        return self.mul_(value)

    def __truediv__(self, value):
        # True div and floor div are the same for Tensor.
        return self.div(value)

    def __rtruediv__(self, value):
        return Tensor.full((), value, self.dtype, self.device) / self

    def __itruediv__(self, value):
        # True div and floor div are the same for Tensor.
        return self.div_(value)

    def __floordiv__(self, value):
        # True div and floor div are the same for Tensor.
        return self.div(value)

    def __rfloordiv__(self, value):
        # True div and floor div are the same for Tensor.
        return Tensor.full((), value, self.dtype, self.device) // self

    def __ifloordiv__(self, value):
        # True div and floor div are the same for Tensor.
        return self.div_(value)

    def _reduction_dim_to_size_vector(self, dim):
        if dim is None:
            return SizeVector(list(range(self.ndim)))
        elif isinstance(dim, int):
            return SizeVector([dim])
        elif isinstance(dim, list) or isinstance(dim, tuple):
            return SizeVector(dim)
        else:
            raise TypeError(
                "dim must be int, list or tuple, but was {}.".format(type(dim)))

    @cast_to_py_tensor
    def sum(self, dim=None, keepdim=False):
        """
        Returns the sum along each the specified dimension `dim`. If `dim` is
        None, the reduction happens for all elements of the tensor. If `dim` is
        a list or tuple, the reduction happens in all of the specified `dim`.
        """
        dim = self._reduction_dim_to_size_vector(dim)
        return super(Tensor, self).sum(dim, keepdim)

    @cast_to_py_tensor
    def mean(self, dim=None, keepdim=False):
        """
        Returns the mean along each the specified dimension `dim`. If `dim` is
        None, the reduction happens for all elements of the tensor. If `dim` is
        a list or tuple, the reduction happens in all of the specified `dim`.
        """
        dim = self._reduction_dim_to_size_vector(dim)
        return super(Tensor, self).mean(dim, keepdim)

    @cast_to_py_tensor
    def prod(self, dim=None, keepdim=False):
        """
        Returns the product along each the specified dimension `dim`. If
        `dim` is None, the reduction happens for all elements of the tensor.
        If `dim` is a list or tuple, the reduction happens in all of the
        specified `dim`.
        """
        dim = self._reduction_dim_to_size_vector(dim)
        return super(Tensor, self).prod(dim, keepdim)

    @cast_to_py_tensor
    def min(self, dim=None, keepdim=False):
        """
        Returns the min along each the specified dimension `dim`. If
        `dim` is None, the reduction happens for all elements of the tensor.
        If `dim` is a list or tuple, the reduction happens in all of the
        specified `dim`.

        Throws exception if the tensor has 0 element.
        """
        dim = self._reduction_dim_to_size_vector(dim)
        return super(Tensor, self).min(dim, keepdim)

    @cast_to_py_tensor
    def max(self, dim=None, keepdim=False):
        """
        Returns the max along each the specified dimension `dim`. If
        `dim` is None, the reduction happens for all elements of the tensor.
        If `dim` is a list or tuple, the reduction happens in all of the
        specified `dim`.

        Throws exception if the tensor has 0 element.
        """
        dim = self._reduction_dim_to_size_vector(dim)
        return super(Tensor, self).max(dim, keepdim)

    @cast_to_py_tensor
    def argmin(self, dim=None):
        """
        Returns minimum index of the tensor along the specified dimension. The
        returned tensor has dtype int64_t, and has the same shape as original
        tensor except that the reduced dimension is removed.

        Only one reduction dimension can be specified. If the specified
        dimension is None, the index is into the flattend tensor.
        """
        if dim is None:
            dim = self._reduction_dim_to_size_vector(list(range(self.ndim)))
        elif isinstance(dim, int):
            dim = self._reduction_dim_to_size_vector([dim])
        else:
            raise TypeError("dim must be int or None, but got {}.".format(dim))
        return super(Tensor, self).argmin_(dim)

    @cast_to_py_tensor
    def argmax(self, dim=None):
        """
        Returns maximum index of the tensor along the specified dimension. The
        returned tensor has dtype int64_t, and has the same shape as original
        tensor except that the reduced dimension is removed.

        Only one reduction dimension can be specified. If the specified
        dimension is None, the index is into the flattend tensor.
        """
        if dim is None:
            dim = self._reduction_dim_to_size_vector(list(range(self.ndim)))
        elif isinstance(dim, int):
            dim = self._reduction_dim_to_size_vector([dim])
        else:
            raise TypeError("dim must be int or None, but got {}.".format(dim))
        return super(Tensor, self).argmax_(dim)

    @cast_to_py_tensor
    def isclose(self, other, rtol=1e-5, atol=1e-8):
        """
        Element-wise test if the tensor value is close to other.
        - If the device is not the same: throws exception.
        - If the dtype is not the same: throws exception.
        - If the shape is not the same: throws exception.
        - For each element in the returned tensor:
          abs(self - other) <= (atol + rtol * abs(other)).
        """
        return super(Tensor, self).isclose(other, rtol, atol)

    def __lt__(self, value):
        return self.lt(value)

    def __le__(self, value):
        return self.le(value)

    def __eq__(self, value):
        return self.eq(value)

    def __ne__(self, value):
        return self.ne(value)

    def __gt__(self, value):
        return self.gt(value)

    def __ge__(self, value):
        return self.ge(value)

    @cast_to_py_tensor
    def item(self):
        """
        Returns scalar value of a scalar Tensor, the Tensor mush have empty
        shape ().
        """
        if self.dtype == Dtype.Float32:
            return super(Tensor, self)._item_float()
        elif self.dtype == Dtype.Float64:
            return super(Tensor, self)._item_double()
        elif self.dtype == Dtype.Int32:
            return super(Tensor, self)._item_int32_t()
        elif self.dtype == Dtype.Int64:
            return super(Tensor, self)._item_int64_t()
        elif self.dtype == Dtype.UInt8:
            return super(Tensor, self)._item_uint8_t()
        elif self.dtype == Dtype.UInt16:
            return super(Tensor, self)._item_uint16_t()
        elif self.dtype == Dtype.Bool:
            return super(Tensor, self)._item_bool()
        else:
            raise TypeError("Unspported type when calling item()")


class Hashmap(o3d.pybind.core.Hashmap):
    """
    Open3D Hashmap class. A Hashmap is a map from key to data wrapped by Tensors.
    """

    def __init__(self, init_capacity, dtype_key, dtype_value, device=None):
        super(Hashmap, self).__init__(init_capacity, dtype_key, dtype_value,
                                      device)

    @cast_to_py_tensor
    def insert(self, keys, values):
        return super(Hashmap, self).insert(keys, values)

    @cast_to_py_tensor
    def find(self, keys):
        return super(Hashmap, self).find(keys)

    @cast_to_py_tensor
    def activate(self, keys):
        return super(Hashmap, self).activate(keys)

    @cast_to_py_tensor
    def erase(self, keys):
        return super(Hashmap, self).erase(keys)

    @cast_to_py_tensor
    def unpack_iterators(self, iterators, masks):
        return super(Hashmap, self).unpack_iterators(iterators, masks)

    @cast_to_py_tensor
    def assign_iterators(self, iterators, values, masks=Tensor([])):
        return super(Hashmap, self).assign_iterators(iterators, values, masks)
