import Navbar from '@/components/navbar'
import styles from '@/styles/product.module.css'
import PrivateRoute from '@/components/private_route';
import { useState } from 'react';
import { useEffect } from 'react';
export default function Product() {
    

  const [flashcard_question,setFlashCardQuestion] = useState(null);
  const [answer,setAnswer] = useState('');
  const  [correct,setCorrect] = useState('');
  const get_question = async () =>{
    try{
      const res = await fetch("https://8000-sslithercod-rlflashcard-ugheinroepa.ws-us92.gitpod.io/generate_question",{
        headers: {
          "Authorization":`Bearer ${localStorage.getItem("acess_token")}`

        }
      });
      if(res.ok){
        let data =  await res.json();
        setFlashCardQuestion(data);
      }
      else{
        console.log("Error: Invalid request");
      }
    }catch(error){
      console.log(error);
    }
   
   
    
}

const check_answer = async (e) =>{
    e.preventDefault();
    const res = await fetch("https://8000-sslithercod-rlflashcard-ugheinroepa.ws-us92.gitpod.io/flashcard/recv_answer",{
      method: 'POST',
      body: JSON.stringify({
        user_answer: answer,
        correct_answer: flashcard_question['answer'],
        question:flashcard_question['question']
      }),headers: {
        "Authorization":`Bearer ${localStorage.getItem("acess_token")}`,
        "Content-Type": "application/json"
      }
      
    })
    if(res.ok){
      let data  = await res.json()
      if(data['correct'] === false){
        setCorrect(`incorrect the answer is ${data['answer']} `)
      }else if(data['correct'] === true){
        setCorrect('correct')
        setTimeout(() => {
          location.reload();
        }, 1000); 
    } else{
      setCorrect('unable to load');
    }

  }

}

  useEffect(() => {
    get_question();
  }, []);
  return (
    <PrivateRoute>
        <div>
            <Navbar/>
                <div className={styles.page}>
                <div className="space"></div>
                <div className={styles.flashcard}>
                    <h1 className={styles.question}>{flashcard_question && "Capital of "+flashcard_question["question"]}</h1>
                    <form action="/product" method="post" autoComplete="off"  id="flashcard_form" onSubmit={check_answer}>
                        <input value={answer} type="text" name="flashcard_question_input" autoComplete="off"  onChange={(e)=>setAnswer(e.target.value) }></input>
                        <button className={styles.submitBttn}  id="submit_button">Answer</button>
                    </form>
                    <p>{correct}</p>
                </div>

                </div>

        </div>
    </PrivateRoute>
        
        
  )
}
