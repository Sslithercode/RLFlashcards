import Navbar from "@/components/navbar";
import { useState } from 'react';
import styles from '@/styles/regform.module.css'
import Link from "next/link"
export default function Login(){
    const [username,setUsername] = useState('');
    const [password,setPassword]  = useState('');

    const login = async (e) =>{
        e.preventDefault();
        const res = await fetch("http://127.0.0.1:5000/login",{
          method: 'POST',
          body: JSON.stringify({
            username: username,
            password: password,
          }),headers: {
            "Content-Type": "application/json"
          }
          
        }) 
        if(res.ok){
          let  auth = await res.json();
          localStorage.setItem('acess_token',auth['access_token']);
          console.log("Logged In");
        }else{
            console.log("Something went wrong");
        }
      
       
      }


      return(
        <div className={styles.page}>
            <Navbar/>
            
            <form action="/" method="post" autoComplete="off"  id="login_form" onSubmit={login}>
                <div className={styles.grid}>
                  
                    <label htmlFor="email_field" className={styles.label}>Email</label>
                    <input value={username} className={styles.input} type="text" name="email_field" id="email_field" autoComplete="off"  onChange={(e)=>setUsername(e.target.value) }></input>
                    <label htmlFor="password_field" className={styles.label}>Password</label>
                    <input value={password} className={styles.input} type="password" name="password_field" id="password_field" autoComplete="off"  onChange={(e)=>setPassword(e.target.value) }></input>
                    <button className={styles.button} id="submit_button">Login</button>
                </div>
            </form>
            <Link href="/register"  className={styles.info}>Click here to register!</Link>
          


        
           

        </div>

        
    );
}
