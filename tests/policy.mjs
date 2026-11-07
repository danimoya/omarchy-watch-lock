import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { test } from 'node:test';

const source = readFileSync(new URL('../Service.qml', import.meta.url),'utf8');
function timer() { return { running:false, restart() { this.running=true; }, stop() { this.running=false; } }; }
function service() {
  const s = {
    stateKnown:true,stayAwake:true,lidClosed:false,watchMode:false,watchPreview:false,previewVisible:false,
    passwordPamConfigured:true,lockRequested:false,powerAllowsScreensaver:true,
    screensaverRunning:false,screensaverCovered:false,screensaverLaunchProcess:{running:false},
    sessionLock:{locked:false,secure:false},idleBlankTimer:{...timer(),idleMs:5000},
    pendingSessionLock:false,enteredPassword:'',resets:0,queued:0,stopped:0,
    Date,Qt:{callLater(fn) { fn(); }},
    resetAuthenticationState() { this.resets++; this.enteredPassword=''; },
    stopScreensaver() { this.stopped++; },runWake() {},
    queueSessionLock() { this.queued++; },refreshBackground() {},refreshFingerprintStatus() {},
    noteSleepRequested() {},logEvent() {},
  };
  for (const [k,v] of Object.entries(s)) if (typeof v==='function' && k!=='Date') s[k]=v.bind(s);
  s.root=s;
  Object.defineProperties(s,{
    locked:{get() { return this.lockRequested||this.sessionLock.locked||this.sessionLock.secure; }},
    liveBackground:{get() { return this.locked && this.stateKnown && !this.lidClosed && (this.watchMode && this.stayAwake || this.screensaverCovered && this.powerAllowsScreensaver); }},
  });
  vm.createContext(s);
  for (const [name,spaces] of [['currentlyLocked',2],['beginLock',2],['armBlankTimer',2],['applyRuntimeState',2],['startIdleScreensaver',2],['watch',4],['lock',4],['idleScreensaver',4]]) {
    const indent=' '.repeat(spaces);
    const match=source.match(new RegExp(`${indent}function ${name}\\([^)]*\\)(?:: string)? \\{[\\s\\S]*?\\n${indent}\\}`));
    assert.ok(match,name);
    vm.runInContext(match[0].replace('): string',')'),s);
  }
  return s;
}

test('watch requests a session lock and keeps the live display on',()=>{
  const s=service(); assert.equal(s.watch(),'ok');
  assert.equal(s.lockRequested,true); assert.equal(s.watchMode,true);
  assert.equal(s.queued,1); assert.equal(s.idleBlankTimer.running,false);
});
test('watch requires known awake state, open lid and configured PAM',()=>{
  for(const [key,value] of [['stateKnown',false],['stayAwake',false],['lidClosed',true],['passwordPamConfigured',false]]) {
    const s=service();s[key]=value;assert.notEqual(s.watch(),'ok',key);assert.equal(s.queued,0,key);
  }
});
test('a normal locked desktop cannot become transparent via watch IPC',()=>{
  const s=service();s.lock();s.sessionLock.secure=true;
  assert.equal(s.watch(),'already-locked');assert.equal(s.watchMode,false);assert.equal(s.sessionLock.secure,true);
});
test('repeated watch requests do not reset password input or authentication',()=>{
  const s=service();s.watch();s.enteredPassword='fixture';s.watch();
  assert.equal(s.enteredPassword,'fixture');assert.equal(s.resets,1);
});
test('system/suspend lock requests hide a watch desktop without unlocking',()=>{
  const s=service();s.watch();s.sessionLock.secure=true;s.lock();
  assert.equal(s.watchMode,false);assert.equal(s.sessionLock.secure,true);assert.equal(s.resets,1);
});
test('runtime failures and disabling awake hide the watch desktop',()=>{
  const s=service();s.watch();s.sessionLock.secure=true;s.applyRuntimeState('invalid');
  assert.equal(s.stateKnown,false);assert.equal(s.watchMode,false);assert.equal(s.sessionLock.secure,true);
});
test('enabling awake while already normally locked does not disclose apps',()=>{
  const s=service();s.stayAwake=false;s.lock();
  s.applyRuntimeState(JSON.stringify({stateKnown:true,stayAwake:true,lidClosed:false,screensaverRunning:false,screensaverCovered:false}));
  assert.equal(s.watchMode,false);assert.equal(s.liveBackground,false);
});
test('idle screensaver hook requires a secure normal lock and safe power/lid',()=>{
  const s=service();s.stayAwake=false;s.lock();
  assert.equal(s.idleScreensaver(),'not-allowed');
  s.sessionLock.secure=true;assert.equal(s.idleScreensaver(),'ok');assert.equal(s.screensaverLaunchProcess.running,true);
  for (const [key,value] of [['watchMode',true],['stayAwake',true],['stateKnown',false],['lidClosed',true],['powerAllowsScreensaver',false]]) {
    const t=service();t.stayAwake=false;t.lock();t.sessionLock.secure=true;t[key]=value;
    assert.equal(t.idleScreensaver(),'not-allowed',key);assert.equal(t.screensaverLaunchProcess.running,false,key);
  }
});
test('normal lock has no watch disclosure and retains ordinary blanking',()=>{
  const s=service();s.lock();assert.equal(s.watchMode,false);assert.equal(s.idleBlankTimer.running,true);
});
test('no preview, watch or idle IPC function directly unlocks',()=>{
  for(const name of ['watch','idleScreensaver','preview','previewWatch','hidePreview']) {
    const body=source.match(new RegExp(`    function ${name}\\([^)]*\\): string \\{[\\s\\S]*?\\n    \\}`))[0];
    assert.doesNotMatch(body,/finishUnlock|sessionLock\.locked\s*=\s*false/);
  }
});
