import {describe,it,expect} from 'vitest';
import {detectAnomalies,initialBuildings,makeAction,rankActions,seedReadings,validateReadings,Settings,Reading} from '../src/engine';
const settings:Settings={campus:'Test',location:'Test',currency:'INR',tariff:8.5,emissionFactor:.716,targetPercent:12,spikeThreshold:25,afterHoursThreshold:1,approvalRequired:true,reportingPeriod:'30 days'};
describe('GreenCampus energy engine',()=>{
 it('seeds 30 days for each of five buildings',()=>{expect(seedReadings()).toHaveLength(150)});
 it('validates readings and flags negative kWh',()=>{const r:Reading[]=[{id:'x',buildingId:'eng',date:'2026-10-15',kwh:-1,baseline:20,source:'demo'}];expect(validateReadings(r).ok).toBe(false);expect(validateReadings(r).invalid).toBe(1)});
 it('detects seeded lab after-hours anomaly and engineering spike',()=>{const f=detectAnomalies(seedReadings(),initialBuildings,settings);expect(f.some(x=>x.buildingId==='lab'&&x.kind==='after-hours')).toBe(true);expect(f.some(x=>x.buildingId==='eng'&&x.kind==='spike')).toBe(true)});
 it('does not divide by zero baseline',()=>{const r:Reading[]=[{id:'z',buildingId:'eng',date:'2026-10-15',kwh:30,baseline:0,source:'demo'}];expect(detectAnomalies(r,initialBuildings,settings)).toHaveLength(0)});
 it('makes action approval-gated and estimates cost/carbon transparently',()=>{const f=detectAnomalies(seedReadings(),initialBuildings,settings)[0];const a=makeAction(f,settings);expect(a.status).toBe('Awaiting Approval');expect(a.costSavings).toBe(Math.round(a.savings*settings.tariff));expect(a.co2).toBe(Math.round(a.savings*settings.emissionFactor*10)/10)});
 it('ranks high-priority actions ahead of low-priority ones',()=>{const base=makeAction(detectAnomalies(seedReadings(),initialBuildings,settings)[0],settings);const ranked=rankActions([{...base,id:'low',priority:'Low'},{...base,id:'high',priority:'High'}]);expect(ranked[0].id).toBe('high')});
});
