import Link from "next/link"
import styles from '@/styles/navbar.module.css'

function Navbar(){
    return(
        <div className={styles.navbar}>
            <img src="/assets/Logo.svg" alt="An SVG of an eye" className="Logo" />
            <li><Link href="/">Home</Link></li>
            <li><Link href="/product">Product</Link></li>
            <li><Link href="/login">Login</Link></li>
            <li><Link href="#">Contribute</Link></li>
            
        </div>
    )
}


export default Navbar;