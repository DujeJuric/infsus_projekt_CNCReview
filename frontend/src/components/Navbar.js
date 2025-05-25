import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

const Navbar = () => {
    const location = useLocation();
    const { pathname } = location;
    console.log(pathname);
    const pattern = /objekt/;

    return (
        <nav className="navbar">
            <ul>
                <li className={pathname === "/" ? "active-link" : ""}><Link to="/">Početna stranica</Link></li>
                <li className={pattern.test(pathname) ? "active-link" : ""}><Link to="/objekti">Objekti</Link></li>
                <li className={pathname === "/gradovi" ? "active-link" : ""}><Link to="/gradovi">Gradovi</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;