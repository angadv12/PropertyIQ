import { useState, useEffect } from "react";
import { FaPencil, FaArrowLeft } from "react-icons/fa6";
import { Link, useNavigate } from "react-router-dom";
import { FadeLoader } from "react-spinners";
import { toast } from "react-toastify"
import 'react-toastify/dist/ReactToastify.css';
import api from "../api";

const EditProfilePage = () => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserDetails = async () => {
        try {
            const response = await api.get('/api/user/details/');
            setUser(response.data);
        } catch (error) {
            toast.error('Error fetching user details.', {
            position: 'top-center',
            autoClose: 5000,
            });
        }
        };

        fetchUserDetails();
    }, []);
    
    const handleChange = (e) => {
        setUser(prevData => ({ ...prevData, [e.target.name]: e.target.value }));
    };
    
    const handleUpdate = async (e) => {
        e.preventDefault();
        const formData = new FormData();
    
        // Append each key-value pair to the FormData object
        Object.keys(user).forEach(key => {
            console.log(key, user[key]);
            formData.append(key, user[key]);
        });
    
        try {
            await api.put('/api/user/details/', formData);
            navigate('/profile');
        } catch (error) {
            console.error('Error updating profile:', error);
            toast.error('Failed to update profile. Please try again.', {
                position: 'top-center',
                autoClose: 5000,
            });
        }
    };
    

    if (!user) {
        return (
          <div className="flex justify-center items-center h-screen">
            <FadeLoader color='#D3D3D3'/>
          </div>
        );
      }

  return (
    <div className="w-screen flex items-center justify-center">
      <div className="rounded-lg shadow-xl p-8 my-6 w-full max-w-2xl">
        <h1 className="font-bold text-4xl flex items-center relative mb-6">
          <Link to="/profile">
            <p className="text-xl flex items-center font-semibold"> <FaArrowLeft className="mr-2"/> Back </p>
          </Link>
          <p className="flex items-center absolute left-1/2 -translate-x-1/2"> <FaPencil className="mr-4" /> Edit Profile </p>
        </h1>
          <form onSubmit={handleUpdate}>
            <div className="flex flex-col items-center">
              <div className="flex items-center w-full">
                <label className="font-semibold text-xl w-1/2 mr-4 mb-3">
                  <p>Username:</p>
                  <input
                    type="text"
                    value={user.username}
                    onChange={handleChange}
                    placeholder="Username"
                    className="block text-gray-900 p-2 rounded w-full -ml-1 border-2 border-gray-300"
                  />
                </label>
                <label className="font-semibold w-1/2 text-xl mb-3 mr-4">
                  <p>Email:</p>
                  <input
                    type="email"
                    value={user.email}
                    onChange={handleChange}
                    placeholder="Email"
                    className="block text-gray-900 p-2 rounded w-full -ml-1 border-2 border-gray-300"
                  />
                </label>
                <label className="font-semibold w-1/2 text-xl mb-3">
                  <p>Password:</p>
                  <input
                    type="password"
                    value={user.password}
                    onChange={handleChange}
                    placeholder="New Password"
                    className="block text-gray-900 px-4 py-2 rounded w-full -ml-1 border-2 border-gray-300"
                  />
                </label>
              </div>
              <button
                type="submit"
                className="mt-4 bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 w-full"
              >
                Update Profile
              </button>
            </div>
          </form>
      </div>
    </div>
  );
};

export default EditProfilePage;