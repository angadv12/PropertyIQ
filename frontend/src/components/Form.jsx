import { useState } from 'react';
import PropTypes from 'prop-types';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';
import { FaArrowRightToBracket } from 'react-icons/fa6';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { FadeLoader } from 'react-spinners';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

function Form({ route, method }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === 'login' ? "Login" : "Register"

    Form.propTypes = {
        route: PropTypes.string.isRequired,
        method: PropTypes.oneOf(['login', 'register']).isRequired,
    };

    const handleSubmit = async (e) => {
        setLoading(true)
        e.preventDefault()

        try {
            const res = await api.post(route, { username, email, password })
            if(method === 'login') {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
                navigate('/')
            } else {
                navigate('/login')
            }
        } catch (error) {
            console.log(error)
            toast.error('Invalid credentials.', { position: 'top-center', autoClose: 5000 })
        } finally {
            setLoading(false)
        }
    }

    const handleGoogleLoginSuccess = async (credentialResponse) => {
        try {
            const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/google-login/`, { 
                token: credentialResponse.credential
            });
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate('/');
        } catch (error) {
            console.error("Google login error:", error);
            toast.error('Google login failed.', { position: 'top-center', autoClose: 5000 });
        }
    };

    const handleGoogleLoginFailure = (error) => {
        console.error("Google login failed:", error);
        toast.error('Google login failed.', { position: 'top-center', autoClose: 5000 });
    };

    if (loading){
        return <FadeLoader />
    }

    return <>
    <div className='w-screen flex justify-center'>
        <form onSubmit={handleSubmit} className='shadow-2xl border-2 flex flex-col items-center justify-center m-12 py-8 px-6 rounded-lg w-1/3 bg-white'>
            <h1 className='font-bold text-3xl mb-4'>{name}</h1>
            {method === 'register' &&
            <input className='w-11/12 p-2 my-2 border-2 border-solid rounded-md box-border mb-2'
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder='Email'
            />
            }
            <input className='w-11/12 p-2 my-2 border-2 border-solid rounded-md box-border mb-2'
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder='Username'
            />
            <input className='w-11/12 p-2 my-2 border-2 border-solid rounded-md box-border mb-4'
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder='Password'
            />
            <button className='w-11/12 p-2 my-2 bg-blue-500 text-white rounded-md cursor-pointer hover:bg-blue-600 flex items-center justify-center'
                type='submit'
            >
                {name} <FaArrowRightToBracket className='ml-2'/>
            </button>

            {method === 'login' && (
                <div className="w-11/12 mt-4">
                    <GoogleLogin
                        onSuccess={handleGoogleLoginSuccess}
                        onError={handleGoogleLoginFailure}
                    />
                </div>
            )}
        </form>
    </div>
    </>
}

export default Form