import './App.css';

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

import { Login } from './pages/Login/Login';
import { Signup } from './pages/Signup/Signup';
import { Home } from './pages/Home/Home';
import { useAuth } from './context/AuthContext';

function App() {

  const { user } = useAuth();

  const ProtectedRoute = ({children}) => {
    console.log(user)
    if (!user) {
      return <Navigate to="/" />
    }
    return children;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
