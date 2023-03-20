import { useRouter } from 'next/router';
import { useEffect } from 'react';

const PrivateRoute = ({ children }) => {
  const router = useRouter();

  useEffect(() => {
    const validateToken = async () => {
      const token = localStorage.getItem('acess_token');
      if (!token) {
        router.push('/login');
      } else {

        try{
            const response = await fetch('http://127.0.0.1:5000/validate_token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (!data.valid) {
          
          router.push('/login');

        }
      }catch(error){
        console.log(error)
      }
        }
        
    };

    validateToken();
  }, [router]);

  return <>{children}</>;
};

export default PrivateRoute;