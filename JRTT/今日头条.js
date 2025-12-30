
function watch(obj, name) {
    return new Proxy(obj,{
        get: function(target, property, receiver) {
            try {
                if (typeof target[property] === "function") {
                    console.table([`对象 => ${name} ,读取属性:`, property + `,值为:` + 'function' + `,类型为:` + (typeof target[property])]);
                } else {
                    console.table([`对象 => ${name} ,读取属性:`, property + `,值为:` + target[property] + `,类型为:` + (typeof target[property])]);
                }
            } catch (e) {}
            return target[property];
        },
        set: function(target, property, newValue, receiver) {
            try {
                console.table([`对象 => ${name} ,设置属性:`, property + `,值为:` + newValue + `,类型为:` + (typeof newValue)]);
            } catch (e) {}
            return Reflect.set(target, property, newValue, receiver);
        }
    });
}
window = global;
window = watch(window, "window");


require('./bdms.js')

arguments = [
    0,
    1,
    12,
    "channel_id=0&max_behot_time=1766479948&offset=0&category=pc_profile_recommend&aid=24&app_name=toutiao_web&msToken=Q6Qb7E-Ek_ta3ceQHSHWgY5hHL4pbegiSqmrNtSLHhcQFN5MCwd5axePPLXQpxr5SnIoSE5mudhuh9mCmXkbrwpSc9vImjbyE0MeCD512H9XzHxgk1R4FaOxyy978Fk%3D&msToken=Q6Qb7E-Ek_ta3ceQHSHWgY5hHL4pbegiSqmrNtSLHhcQFN5MCwd5axePPLXQpxr5SnIoSE5mudhuh9mCmXkbrwpSc9vImjbyE0MeCD512H9XzHxgk1R4FaOxyy978Fk%3D",
    "",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
]

r = window.uuuu.v
a_bours = window.uuuu._u = (r[0], arguments, r[1], r[2], this)
console.log(a_bours)
