use pyo3::{prelude::*, types::PyBytes};
use paxect_core_rs as pax; // veilige alias (niet 'core', dat botst met std core)

#[pyfunction]
fn encode_py(py: Python<'_>, data: &[u8]) -> PyResult<Py<PyBytes>> {
    let out = pax::encode(data);
    Ok(PyBytes::new(py, &out).into())
}

#[pyfunction]
fn decode_py(py: Python<'_>, data: &[u8]) -> PyResult<Py<PyBytes>> {
    match pax::decode(data) {
        Ok(out) => Ok(PyBytes::new(py, &out).into()),
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e)),
    }
}

#[pymodule]
fn paxect_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode_py, m)?)?;
    m.add_function(wrap_pyfunction!(decode_py, m)?)?;
    Ok(())
}
