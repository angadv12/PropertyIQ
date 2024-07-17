import { Outlet } from "react-router-dom"
import Navbar from "../components/Navbar"

const MainLayout = () => {
  return (
    <main className="min-h-screen pt-20">
        <Navbar />
        <Outlet />
    </main>
  )
}
export default MainLayout