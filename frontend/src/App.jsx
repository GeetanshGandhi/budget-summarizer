import { useEffect, useRef, useState } from 'react';
import './App.css';
function App() {
	const myRef = useRef(null)
	const fyearList= ["2024-25","2023-24","2022-23","2021-22","2020-21","2019-20","2018-19","2017-18","2016-17"]
	const [summary, setSummary] = useState(null)
	const yearMap = {"2024_25":"2024-25", "2023_24":"2023-24", "2022_23":"2022-23",
		"2021_22":"2021-22", "2020_21":"2020-21", "2019_20":"2019-20", "2018_19":"2018-19",
		"2017_18":"2017-18", "2016_17":"2016-17"
	}
	const [fyear, setfyear] = useState("2024-25")
	useEffect(()=>{
		const yearselect = document.getElementById("fyear-selection")
		fyearList.forEach((item)=>{
			let valueString = item.substring(0,4)+"_"+item.substring(5,7)
			let option = `<option ${item==="2024-25" && "selected"} value=${valueString}>${item}</option>`
			yearselect.insertAdjacentHTML("beforeend", option)
		})
	},[])
	const changeFyear = async()=> {
		setfyear(yearMap[document.getElementById("fyear-selection").value])
		let response = await fetch("http://127.0.0.1:5000/fetchSummary",{
			body: JSON.stringify(fyear),
			headers: {"content-type":"application/json"},
			method: "POST"
		})
		let res = await response.json()
		setSummary(res)
		setTimeout(()=>{
			window.scrollTo({top: myRef.current.offsetTop, behavior:"smooth"})
		},500)
	}
	return (
		<>
		<div className='home'>
			<div className="container">
				<h1 className="main-head">Budget Summarize<span className='rupee'>₹</span></h1>
				<div className="wrapper">
					<p className="fyear-msg">Select Financial Year:</p>
					<select onChange={changeFyear} id="fyear-selection"></select>
				</div>
			</div>
		</div>
		{
			summary !== null &&
			<div ref={myRef} className="summary-container">
				<h2 className="summary-head">Summary for Budget (FY: {fyear})</h2>
				{
				Object.keys(summary).map((item)=>{
					return <div className='cat-container'>
						<p className="sub-head">{item}</p>
						{
							summary[item].map((fact)=>{
								return <>
									<p className='fact'>• {fact}</p>
								</>
							})
						}
					</div>
				})
				}
			</div>
		}
		</>
	)
}
export default App;