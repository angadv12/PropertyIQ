import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ListingsPage from './pages/ListingsPage';
import EditListingPage from './pages/EditListingPage';
import NotFoundPage from './pages/NotFoundPage';
import DetailsPage from './pages/DetailsPage';
import OtherDetailsPage from './pages/OtherDetailsPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import MainLayout from './layouts/MainLayout';
import EditProfilePage from './pages/EditProfilePage';

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <RegisterPage/>
}

function App() {
  const router = createBrowserRouter(createRoutesFromElements(
    <>
      <Route path='/' element={ <MainLayout />}>
        <Route index element={<HomePage />} />,
        <Route path="/listings" element={<ProtectedRoute> <ListingsPage /> </ProtectedRoute>} />
        <Route path="/login" element={<LoginPage />} />,
        <Route path="/logout" element={<ProtectedRoute> <Logout /> </ProtectedRoute>} />,
        <Route path="/register" element={<RegisterAndLogout />} />,
        <Route path="/listings/:listingId/edit" element={<ProtectedRoute> <EditListingPage /> </ProtectedRoute>} />,
        <Route path="/profile" element={<ProtectedRoute> <ProfilePage /> </ProtectedRoute>} />,
        <Route path="/profile/edit" element={<ProtectedRoute> <EditProfilePage /> </ProtectedRoute>} />,
        <Route path='/listings/:listingId' element={<ProtectedRoute> <DetailsPage /> </ProtectedRoute>}/>,
        <Route path='/other/listings/:listingId' element={<ProtectedRoute> <OtherDetailsPage /> </ProtectedRoute>}/>,
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </>
  ))

  return (
    <RouterProvider router={ router } />
  )
}

export default App
