import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { FaSignOutAlt, FaTrashAlt } from 'react-icons/fa';
import { FaPencil } from 'react-icons/fa6';
import { FadeLoader } from 'react-spinners';

const ProfilePage = () => {
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

  const handleDeleteAccount = async () => {
    const confirmed = window.confirm(
      'Are you sure you want to delete your account?'
    );
    if (confirmed) {
      try {
        await api.delete('/api/user/delete/');
        toast.success('Account deleted successfully.', {
          position: 'top-center',
          autoClose: 5000,
        });
        navigate('/login');
      } catch (error) {
        toast.error('Error deleting account.', {
          position: 'top-center',
          autoClose: 5000,
        });
      }
    }
  };

  const handleLogout = () => {
    const confirmed = window.confirm('Are you sure you want to logout?');
    if (confirmed) {
      navigate('/logout');
    }
  };

  if (!user) {
    return (
      <div className="flex justify-center items-center h-screen">
        <FadeLoader color='#000000'/>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-3xl mx-auto bg-white border-2 shadow-lg rounded-lg overflow-hidden">
        <div className="p-8">
          <h1 className="text-4xl font-bold mb-4">Profile Details</h1>
          <div className="mb-4 text-2xl">
            <p>
              <strong>Username:</strong> {user.username}
            </p>
            <p>
              <strong>Email:</strong> {user.email}
            </p>
            <p>
              <strong>ID:</strong> {user.id}
            </p>
          </div>
          <div className="flex space-x-4 mt-8">
            <button
              className="flex items-center bg-green-500 px-4 py-2 rounded-lg text-white hover:bg-green-600 transition-colors"
              onClick={() => navigate('/profile/edit')}
            >
              <FaPencil className="mr-2" /> Edit Account
            </button>
            <button
              className="flex items-center bg-red-500 px-4 py-2 rounded-lg text-white hover:bg-red-600 transition-colors"
              onClick={handleDeleteAccount}
            >
              <FaTrashAlt className="mr-2" /> Delete Account
            </button>
            <button
              className="flex items-center bg-blue-500 px-4 py-2 rounded-lg text-white hover:bg-blue-600 transition-colors"
              onClick={handleLogout}
            >
              <FaSignOutAlt className="mr-2" /> Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
