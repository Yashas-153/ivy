# global
from hypothesis import strategies as st
import ivy

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


@st.composite
def _get_minval_maxval(draw):
    interval = draw(st.integers(min_value=1, max_value=50))
    minval = draw(st.floats(min_value=-100, max_value=100))
    maxval = draw(st.floats(min_value=-100 + interval, max_value=100 + interval))
    return minval, maxval


@handle_frontend_test(
    fn_tree="jax.random.uniform",
    dtype_key=helpers.dtype_and_values(
        available_dtypes=["uint32"],
        min_value=0,
        max_value=2000,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
        max_dim_size=2,
    ),
    shape=helpers.get_shape(),
    dtype=helpers.get_dtypes("float", full=False),
    dtype_minval_maxval=_get_minval_maxval(),
)
def test_jax_uniform(
    *,
    dtype_key,
    shape,
    dtype,
    dtype_minval_maxval,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, key = dtype_key
    minval, maxval = dtype_minval_maxval

    def call():
        return helpers.test_frontend_function(
            input_dtypes=input_dtype,
            frontend=frontend,
            test_flags=test_flags,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            key=key[0],
            shape=shape,
            dtype=dtype[0],
            minval=minval,
            maxval=maxval,
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape


@handle_frontend_test(
    fn_tree="jax.random.normal",
    dtype_key=helpers.dtype_and_values(
        available_dtypes=["uint32"],
        min_value=0,
        max_value=2000,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
        max_dim_size=2,
    ),
    shape=helpers.get_shape(),
    dtype=helpers.get_dtypes("float", full=False),
)
def test_jax_normal(
    *,
    dtype_key,
    shape,
    dtype,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, key = dtype_key

    def call():
        return helpers.test_frontend_function(
            input_dtypes=input_dtype,
            frontend=frontend,
            test_flags=test_flags,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            key=key[0],
            shape=shape,
            dtype=dtype[0],
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape


@handle_frontend_test(
    fn_tree="jax.random.beta",
    dtype_key=helpers.dtype_and_values(
        available_dtypes=["uint32"],
        min_value=0,
        max_value=2000,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
        max_dim_size=2,
    ),
    alpha=st.floats(min_value=0, max_value=5, exclude_min=True),
    beta=st.floats(min_value=0, max_value=5, exclude_min=True),
    shape=helpers.get_shape(
        min_num_dims=2, max_num_dims=2, min_dim_size=1, max_dim_size=5
    ),
    dtype=helpers.get_dtypes("float", full=False),
    test_with_out=st.just(False),
)
def test_jax_beta(
    *,
    dtype_key,
    alpha,
    beta,
    shape,
    dtype,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, key = dtype_key

    def call():
        return helpers.test_frontend_function(
            input_dtypes=input_dtype,
            frontend=frontend,
            test_flags=test_flags,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            key=key[0],
            a=alpha,
            b=beta,
            shape=shape,
            dtype=dtype[0],
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape


@handle_frontend_test(
    fn_tree="jax.random.dirichlet",
    dtype_key=helpers.dtype_and_values(
        available_dtypes=["uint32"],
        min_value=0,
        max_value=2000,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
        max_dim_size=2,
    ),
    dtype_alpha=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float", full=False),
        shape=st.tuples(
            st.integers(min_value=2, max_value=5),
        ),
        min_value=1.1,
        max_value=100.0,
        exclude_min=True,
    ),
    shape=helpers.get_shape(
        min_num_dims=2, max_num_dims=2, min_dim_size=2, max_dim_size=5
    ),
    dtype=helpers.get_dtypes("float", full=False),
    test_with_out=st.just(False),
)
def test_jax_dirichlet(
    *,
    dtype_key,
    dtype_alpha,
    shape,
    dtype,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, key = dtype_key
    _, alpha = dtype_alpha

    def call():
        return helpers.test_frontend_function(
            input_dtypes=input_dtype,
            frontend=frontend,
            test_flags=test_flags,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            key=key[0],
            alpha=alpha[0],
            shape=shape,
            dtype=dtype[0],
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape


@handle_frontend_test(
    fn_tree="jax.random.poisson",
    dtype_key=helpers.dtype_and_values(
        available_dtypes=["uint32"],
        min_value=0,
        max_value=2000,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
        max_dim_size=2,
    ),
    lam=st.floats(min_value=0, max_value=5, exclude_min=True),
    shape=helpers.get_shape(
        min_num_dims=2, max_num_dims=2, min_dim_size=1, max_dim_size=5
    ),
    dtype=helpers.get_dtypes("integer", full=False),
    test_with_out=st.just(False),
)
def test_jax_poisson(
    *,
    dtype_key,
    lam,
    shape,
    dtype,
    on_device,
    fn_tree,
    frontend,
    test_flags,
):
    input_dtype, key = dtype_key

    def call():
        return helpers.test_frontend_function(
            input_dtypes=input_dtype,
            frontend=frontend,
            test_flags=test_flags,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            key=key[0],
            lam=lam,
            shape=shape,
            dtype=dtype[0],
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape
