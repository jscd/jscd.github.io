// Select full email on click
const m=document.getElementById("m");
m.addEventListener('click',function(event){
	if(document.body.createTextRange){
		const r=document.body.createTextRange();
		r.moveToElementText(m);
		r.select()
	}else if(window.getSelection){
		const s=window.getSelection();
		const r=document.createRange();
		r.selectNodeContents(m);
		s.removeAllRanges();
		s.addRange(r)
	}
});
