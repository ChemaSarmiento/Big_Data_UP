(() => {
  'use strict';
  const stage=document.getElementById('stage');
  const viewport=document.getElementById('viewport');
  function fit(){
    if(innerWidth<=700){stage.style.transform='none';return;}
    const scale=Math.min(viewport.clientWidth/1600,viewport.clientHeight/900);
    stage.style.transform=`scale(${scale})`;
    stage.style.left=`${(viewport.clientWidth-1600*scale)/2}px`;
    stage.style.top=`${(viewport.clientHeight-900*scale)/2}px`;
  }
  addEventListener('resize',fit);document.fonts.ready.then(fit);fit();
  addEventListener('hashchange',()=>{viewport.scrollTop=0;});
})();
