// @snippet scene-setnodesradii
auto callable = %PYARG_3;
const std::function<int (qreal)> &func = [callable](qreal value) -> int
{
    if (!PyCallable_Check(callable)) {
        qWarning("Argument 3 of %FUNCTION_NAME must be a callable.");
        return 0;
    }
    Shiboken::GilState state;
    Shiboken::AutoDecRef arglist(PyTuple_New(1));
    PyTuple_SET_ITEM(arglist, 0, Shiboken::Conversions::copyToPython(Shiboken::Conversions::PrimitiveTypeConverter<qreal>(), &value));
    PyObject *result = PyObject_CallObject(callable, arglist);
    float cppResult = 0;
    PythonToCppFunc pythonToCpp = 0;
    if (PyErr_Occurred())
        PyErr_Print();
    else if ((pythonToCpp = Shiboken::Conversions::isPythonToCppConvertible(Shiboken::Conversions::PrimitiveTypeConverter<float>(), result)))
        pythonToCpp(result, &cppResult);
    return int(cppResult);

};
%CPPSELF.%FUNCTION_NAME(%1, %2, func, %4);
// @snippet scene-setnodesradii