const UINT32_SIZE=0x100000000;

function cryptoUint32(){
  const source=globalThis.crypto;
  if(!source?.getRandomValues)return null;
  const values=new Uint32Array(1);source.getRandomValues(values);return values[0];
}

// Browser sessions use the platform CSPRNG; the fallback keeps injected/test
// environments usable when Web Crypto is unavailable.
export function randomFloat(){
  const value=cryptoUint32();return value===null?Math.random():value/UINT32_SIZE;
}

export function randomInt(max,random=randomFloat){
  if(!Number.isSafeInteger(max)||max<1)throw Error('亂數範圍無效。');
  if(random===randomFloat){
    const limit=UINT32_SIZE-(UINT32_SIZE%max);let value;
    do{value=cryptoUint32();}while(value!==null&&value>=limit);
    if(value!==null)return value%max;
  }
  const unit=Number(random());
  if(!Number.isFinite(unit))throw Error('亂數來源無效。');
  return Math.min(max-1,Math.max(0,Math.floor(Math.max(0,unit)*max)));
}

export function shuffle(items,random=randomFloat){
  const result=items.slice();
  for(let i=result.length-1;i>0;i--){const j=randomInt(i+1,random);[result[i],result[j]]=[result[j],result[i]];}
  return result;
}
