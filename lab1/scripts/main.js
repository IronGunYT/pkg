// global variable that stores current selected color
let color = '#8EB8E5';

// region get colors from color variable
function get_RGB() {
    let r = parseInt(color.slice(1, 3), 16);
    let g = parseInt(color.slice(3, 5), 16);
    let b = parseInt(color.slice(5, 7), 16);
    return {
        r: r,
        g: g,
        b: b
    };
}

function get_CMYK() {
    let rgb = get_RGB();
    let r = rgb.r, g = rgb.g, b = rgb.b;
    if(r === 0 && g === 0 && b === 0)
        return {
            c: 0,
            m: 0,
            y: 0,
            k: 100
        }
    let k = Math.min(1-r/255, 1-g/255, 1-b/255);
    let c = (1-r/255-k)/(1-k);
    let m = (1-g/255-k)/(1-k);
    let y = (1-b/255-k)/(1-k);
    return {
        c: Math.round(c*100),
        m: Math.round(m*100),
        y: Math.round(y*100),
        k: Math.round(k*100)
    };
}

function get_HSL() {
    let rgb = get_RGB();
    let r = rgb.r / 255;
    let g = rgb.g / 255;
    let b = rgb.b / 255;

    let max = Math.max(r, g, b);
    let min = Math.min(r, g, b);

    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
        let d = max - min;
        s = d / (1 - Math.abs(2*l - 1));

        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }

        h /= 6;
    }

    h = Math.round(h * 360);
    s = Math.round(s * 100);
    l = Math.round(l * 100);

    return {
        h: h,
        s: s,
        l: l
    };
}

function get_HSV() {
    let rgb = get_RGB();
    let r = rgb.r / 255;
    let g = rgb.g / 255;
    let b = rgb.b / 255;

    let max = Math.max(r, g, b);
    let min = Math.min(r, g, b);

    let h, s, v = max;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
        let d = max - min;
        s = d / max;

        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }

        h /= 6;
    }

    h = Math.round(h * 360);
    s = Math.round(s * 100);
    v = Math.round(v * 100);

    return {
        h: h,
        s: s,
        v: v
    };
}

function get_XYZ() {
    let rgb = get_RGB();
    let r = rgb.r / 255;
    let g = rgb.g / 255;
    let b = rgb.b / 255;

    if (r > 0.04045) {
        r = Math.pow(((r + 0.055) / 1.055), 2.4);
    } else {
        r = r / 12.92;
    }

    if (g > 0.04045) {
        g = Math.pow(((g + 0.055) / 1.055), 2.4);
    } else {
        g = g / 12.92;
    }

    if (b > 0.04045) {
        b = Math.pow(((b + 0.055) / 1.055), 2.4);
    } else {
        b = b / 12.92;
    }

    r *= 100;
    g *= 100;
    b *= 100;

    const x = r * 0.4124 + g * 0.3576 + b * 0.1805;
    const y = r * 0.2126 + g * 0.7152 + b * 0.0722;
    const z = r * 0.0193 + g * 0.1192 + b * 0.9505;

    return {
        x: Math.round(x),
        y: Math.round(y),
        z: Math.round(z)
    };
}

function get_LAB() {
    let xyz = get_XYZ();
    let x = xyz.x / 95.047;
    let y = xyz.y / 100.000;
    let z = xyz.z / 108.883;

    if (x > 0.008856) {
        x = Math.pow(x, 0.333333333);
    } else {
        x = 7.787 * x + 0.137931034;
    }

    if (y > 0.008856) {
        y = Math.pow(y, 0.333333333);
    } else {
        y = 7.787 * y + 0.137931034;
    }

    if (z > 0.008856) {
        z = Math.pow(z, 0.333333333);
    } else {
        z = 7.787 * z + 0.137931034;
    }

    const l = (116 * y) - 16;
    const a = 500 * (x - y);
    const b = 200 * (y - z);

    return {
        l: Math.round(l),
        a: Math.round(a),
        b: Math.round(b)
    };
}
// endregion

function sync_colors(locked_palette) {
    // set current color to all color inputs
    $('#color_picker').val(color);
    $('#color_picker_display').css('background-color', color);
    $('#hex_input').val(color.slice(1, 7));
    $('#rgb_r_input').val(get_RGB().r);
    $('#rgb_r_range').val(get_RGB().r);
    $('#rgb_g_input').val(get_RGB().g);
    $('#rgb_g_range').val(get_RGB().g);
    $('#rgb_b_input').val(get_RGB().b);
    $('#rgb_b_range').val(get_RGB().b);
    $('#cmyk_c_input').val(get_CMYK().c);
    $('#cmyk_c_range').val(get_CMYK().c);
    $('#cmyk_m_input').val(get_CMYK().m);
    $('#cmyk_m_range').val(get_CMYK().m);
    $('#cmyk_y_input').val(get_CMYK().y);
    $('#cmyk_y_range').val(get_CMYK().y);
    $('#cmyk_k_input').val(get_CMYK().k);
    $('#cmyk_k_range').val(get_CMYK().k);
    $('#hsl_h_input').val(get_HSL().h);
    $('#hsl_h_range').val(get_HSL().h);
    $('#hsl_s_input').val(get_HSL().s);
    $('#hsl_s_range').val(get_HSL().s);
    $('#hsl_l_input').val(get_HSL().l);
    $('#hsl_l_range').val(get_HSL().l);
    $('#hsv_h_input').val(get_HSV().h);
    $('#hsv_h_range').val(get_HSV().h);
    $('#hsv_s_input').val(get_HSV().s);
    $('#hsv_s_range').val(get_HSV().s);
    $('#hsv_v_input').val(get_HSV().v);
    $('#hsv_v_range').val(get_HSV().v);
    $('#xyz_x_input').val(get_XYZ().x);
    $('#xyz_x_range').val(get_XYZ().x);
    $('#xyz_y_input').val(get_XYZ().y);
    $('#xyz_y_range').val(get_XYZ().y);
    $('#xyz_z_input').val(get_XYZ().z);
    $('#xyz_z_range').val(get_XYZ().z);
    $('#lab_l_input').val(get_LAB().l);
    $('#lab_l_range').val(get_LAB().l);
    $('#lab_a_input').val(get_LAB().a);
    $('#lab_a_range').val(get_LAB().a);
    $('#lab_b_input').val(get_LAB().b);
    $('#lab_b_range').val(get_LAB().b);

    // set disabled to part of inputs when gray color
    let rgb = get_RGB();
    if (rgb.r === rgb.g && rgb.g === rgb.b) {
        // lock hue
        $('#hsl_h_input').prop('disabled', true);
        $('#hsl_h_range').prop('disabled', true);
        $('#hsv_h_input').prop('disabled', true);
        $('#hsv_h_range').prop('disabled', true);
        // lock cmy
        $('#cmyk_c_input').prop('disabled', true);
        $('#cmyk_c_range').prop('disabled', true);
        $('#cmyk_m_input').prop('disabled', true);
        $('#cmyk_m_range').prop('disabled', true);
        $('#cmyk_y_input').prop('disabled', true);
        $('#cmyk_y_range').prop('disabled', true);
    }else{
        // unlock hue
        $('#hsl_h_input').prop('disabled', false);
        $('#hsl_h_range').prop('disabled', false);
        $('#hsv_h_input').prop('disabled', false);
        $('#hsv_h_range').prop('disabled', false);
        // unlock cmy
        $('#cmyk_c_input').prop('disabled', false);
        $('#cmyk_c_range').prop('disabled', false);
        $('#cmyk_m_input').prop('disabled', false);
        $('#cmyk_m_range').prop('disabled', false);
        $('#cmyk_y_input').prop('disabled', false);
        $('#cmyk_y_range').prop('disabled', false);
    }
}

// region convert all to HEX
function number_to_HEX_part(n) {
    n = n.toString(16);
    return n.length === 1 ? "0"+n : n;
}

function RGB_to_HEX(r, g, b) {
    r = parseInt(r);
    g = parseInt(g);
    b = parseInt(b);
    return '#'+number_to_HEX_part(r)+number_to_HEX_part(g)+number_to_HEX_part(b);
}

function CMYK_to_HEX(c, m, y, k) {
    c = parseInt(c);
    m = parseInt(m);
    y = parseInt(y);
    k = parseInt(k);
    // saving cmyk in decimal values
    c /= 100;
    m /= 100;
    y /= 100;
    k /= 100;
    // convert to RGB, then to HEX
    let r = Math.round(255*(1-c)*(1-k));
    let g = Math.round(255*(1-m)*(1-k));
    let b = Math.round(255*(1-y)*(1-k));
    return RGB_to_HEX(r, g, b);
}

function HSL_to_HEX(h, s, l) {
    h = parseInt(h);
    s = parseInt(s);
    l = parseInt(l);
    // saving hsl in decimal values
    s /= 100;
    l /= 100;

    let c = (1 - Math.abs(2 * l - 1)) * s;
    let x = c * (1 - Math.abs(((h / 60) % 2) - 1));
    let m = l - c / 2;
    let r, g, b;

    if (0 <= h && h < 60) {
        r = c;
        g = x;
        b = 0;
    } else if (60 <= h && h < 120) {
        r = x;
        g = c;
        b = 0;
    } else if (120 <= h && h < 180) {
        r = 0;
        g = c;
        b = x;
    } else if (180 <= h && h < 240) {
        r = 0;
        g = x;
        b = c;
    } else if (240 <= h && h < 300) {
        r = x;
        g = 0;
        b = c;
    } else {
        r = c;
        g = 0;
        b = x;
    }

    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);

    return RGB_to_HEX(r, g, b);
}

function HSV_to_HEX(h, s, v) {
    h = parseInt(h);
    s = parseInt(s);
    v = parseInt(v);
    // saving hsl in decimal values
    s /= 100;
    v /= 100;

    let c = v * s;
    let x = c * (1 - Math.abs(((h / 60) % 2) - 1));
    let m = v - c;
    let r, g, b;

    if (0 <= h && h < 60) {
        r = c;
        g = x;
        b = 0;
    } else if (60 <= h && h < 120) {
        r = x;
        g = c;
        b = 0;
    } else if (120 <= h && h < 180) {
        r = 0;
        g = c;
        b = x;
    } else if (180 <= h && h < 240) {
        r = 0;
        g = x;
        b = c;
    } else if (240 <= h && h < 300) {
        r = x;
        g = 0;
        b = c;
    } else {
        r = c;
        g = 0;
        b = x;
    }

    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);

    return RGB_to_HEX(r, g, b);
}

function XYZ_to_HEX(x, y, z) {
    x = x / 100 // X from 0 to 95.047
    y = y / 100 // Y from 0 to 100.000
    z = z / 100 // Z from 0 to 108.883

    let r = x * 3.2406 + y * -1.5372 + z * -0.4986
    let g = x * -0.9689 + y * 1.8758 + z * 0.0415
    let b = x * 0.0557 + y * -0.2040 + z * 1.0570

    if (r > 0.0031308) {
        r = 1.055 * (Math.pow(r, 0.41666667)) - 0.055
    } else {
        r = 12.92 * r
    }

    if (g > 0.0031308) {
        g = 1.055 * (Math.pow(g, 0.41666667)) - 0.055
    } else {
        g = 12.92 * g
    }

    if (b > 0.0031308) {
        b = 1.055 * (Math.pow(b, 0.41666667)) - 0.055
    } else {
        b = 12.92 * b
    }

    r *= 255
    g *= 255
    b *= 255
    return RGB_to_HEX(r, g, b);
}

function LAB_to_HEX(l, a, b) {
    let y = (l + 16) / 116;
    let x = a / 500 + y;
    let z = y - b / 200;

    if (Math.pow(y, 3) > 0.008856) {
        y = Math.pow(y, 3);
    } else {
        y = (y - 0.137931034) / 7.787;
    }

    if (Math.pow(x, 3) > 0.008856) {
        x = Math.pow(x, 3);
    } else {
        x = (x - 0.137931034) / 7.787;
    }

    if (Math.pow(z, 3) > 0.008856) {
        z = Math.pow(z, 3);
    } else {
        z = (z - 0.137931034) / 7.787;
    }

    x = 95.047 * x;
    y = 100.000 * y;
    z = 108.883 * z;
    return XYZ_to_HEX(x, y, z);
}
// endregion

// region trigger color change
function click_color() {
    console.log("color changed by input:color");
    color = $('#color_picker').val();
    sync_colors();
}

function hex_change() {
    let hex = '#'+$('#hex_input').val();
    if (!/^#[0-9A-F]{6}$/i.test(hex))
        return;
    console.log("color changed by hex_input");
    color = hex;
    sync_colors();
}

function rgb_r_change() {
    let r = parseInt($('#rgb_r_input').val());
    if (r < 0 || r > 255 || isNaN(r))
        return;
    console.log("color changed by rgb_r_input");
    let rgb = get_RGB();
    color = RGB_to_HEX(r, rgb.g, rgb.b);
    sync_colors();
}

function rgb_r_range_change() {
    let r = parseInt($('#rgb_r_range').val());
    if (r < 0 || r > 255 || isNaN(r))
        return;
    console.log("color changed by rgb_r_range");
    let rgb = get_RGB();
    color = RGB_to_HEX(r, rgb.g, rgb.b);
    sync_colors();
}

function rgb_g_change() {
    let g = parseInt($('#rgb_g_input').val());
    if (g < 0 || g > 255 || isNaN(g))
        return;
    console.log("color changed by rgb_g_input");
    let rgb = get_RGB();
    color = RGB_to_HEX(rgb.r, g, rgb.b);
    sync_colors();
}

function rgb_g_range_change() {
    let g = parseInt($('#rgb_g_range').val());
    if (g < 0 || g > 255 || isNaN(g))
        return;
    console.log("color changed by rgb_g_range");
    let rgb = get_RGB();
    color = RGB_to_HEX(rgb.r, g, rgb.b);
    sync_colors();
}

function rgb_b_change() {
    let b = parseInt($('#rgb_b_input').val());
    if (b < 0 || b > 255 || isNaN(b))
        return;
    console.log("color changed by rgb_b_input");
    let rgb = get_RGB();
    color = RGB_to_HEX(rgb.r, rgb.g, b);
    sync_colors();
}

function rgb_b_range_change() {
    let b = parseInt($('#rgb_b_range').val());
    if (b < 0 || b > 255 || isNaN(b))
        return;
    console.log("color changed by rgb_b_range");
    let rgb = get_RGB();
    color = RGB_to_HEX(rgb.r, rgb.g, b);
    sync_colors();
}

function cmyk_c_change() {
    let c = parseInt($('#cmyk_c_input').val());
    if (c < 0 || c > 100 || isNaN(c))
        return;
    console.log("color changed by cmyk_c_input");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(c, cmyk.m, cmyk.y, cmyk.k);
    sync_colors();
}

function cmyk_c_range_change() {
    let c = parseInt($('#cmyk_c_range').val());
    if (c < 0 || c > 100 || isNaN(c))
        return;
    console.log("color changed by cmyk_c_range");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(c, cmyk.m, cmyk.y, cmyk.k);
    sync_colors();
}

function cmyk_m_change() {
    let m = parseInt($('#cmyk_m_input').val());
    if (m < 0 || m > 100 || isNaN(m))
        return;
    console.log("color changed by cmyk_m_input");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(cmyk.c, m, cmyk.y, cmyk.k);
    sync_colors();
}

function cmyk_m_range_change() {
    let m = parseInt($('#cmyk_m_range').val());
    if (m < 0 || m > 100 || isNaN(m))
        return;
    console.log("color changed by cmyk_m_range");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(cmyk.c, m, cmyk.y, cmyk.k);
    sync_colors();
}

function cmyk_y_change() {
    let y = parseInt($('#cmyk_y_input').val());
    if (y < 0 || y > 100 || isNaN(y))
        return;
    console.log("color changed by cmyk_y_input");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(cmyk.c, cmyk.m, y, cmyk.k);
    sync_colors();
}

function cmyk_y_range_change() {
    let y = parseInt($('#cmyk_y_range').val());
    if (y < 0 || y > 100 || isNaN(y))
        return;
    console.log("color changed by cmyk_y_range");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(cmyk.c, cmyk.m, y, cmyk.k);
    sync_colors();
}

function cmyk_k_change() {
    let k = parseInt($('#cmyk_k_input').val());
    if (k < 0 || k > 100 || isNaN(k))
        return;
    console.log("color changed by cmyk_k_input");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(cmyk.c, cmyk.m, cmyk.y, k);
    sync_colors();
}

function cmyk_k_range_change() {
    let k = parseInt($('#cmyk_k_range').val());
    if (k < 0 || k > 100 || isNaN(k))
        return;
    console.log("color changed by cmyk_k_range");
    let cmyk = get_CMYK();
    color = CMYK_to_HEX(cmyk.c, cmyk.m, cmyk.y, k);
    sync_colors();
}

function hsl_h_change() {
    let h = parseInt($('#hsl_h_input').val());
    if (h < 0 || h > 360 || isNaN(h))
        return;
    console.log("color changed by hsl_h_input");
    let hsl = get_HSL();
    color = HSL_to_HEX(h, hsl.s, hsl.l);
    sync_colors();
}

function hsl_h_range_change() {
    let h = parseInt($('#hsl_h_range').val());
    if (h < 0 || h > 360 || isNaN(h))
        return;
    console.log("color changed by hsl_h_range");
    let hsl = get_HSL();
    color = HSL_to_HEX(h, hsl.s, hsl.l);
    sync_colors();
}

function hsl_s_change() {
    let s = parseInt($('#hsl_s_input').val());
    if (s < 0 || s > 100 || isNaN(s))
        return;
    console.log("color changed by hsl_s_input");
    let hsl = get_HSL();
    color = HSL_to_HEX(hsl.h, s, hsl.l);
    sync_colors();
}

function hsl_s_range_change() {
    let s = parseInt($('#hsl_s_range').val());
    if (s < 0 || s > 100 || isNaN(s))
        return;
    console.log("color changed by hsl_s_range");
    let hsl = get_HSL();
    color = HSL_to_HEX(hsl.h, s, hsl.l);
    sync_colors();
}

function hsl_l_change() {
    let l = parseInt($('#hsl_l_input').val());
    if (l < 0 || l > 100 || isNaN(l))
        return;
    console.log("color changed by hsl_l_input");
    let hsl = get_HSL();
    color = HSL_to_HEX(hsl.h, hsl.s, l);
    sync_colors();
}

function hsl_l_range_change() {
    let l = parseInt($('#hsl_l_range').val());
    if (l < 0 || l > 100 || isNaN(l))
        return;
    console.log("color changed by hsl_l_range");
    let hsl = get_HSL();
    color = HSL_to_HEX(hsl.h, hsl.s, l);
    sync_colors();
}

function hsv_h_change() {
    let h = parseInt($('#hsv_h_input').val());
    if (h < 0 || h > 360 || isNaN(h))
        return;
    console.log("color changed by hsv_h_input");
    let hsv = get_HSV();
    color = HSV_to_HEX(h, hsv.s, hsv.v);
    sync_colors();
}

function hsv_h_range_change() {
    let h = parseInt($('#hsv_h_range').val());
    if (h < 0 || h > 360 || isNaN(h))
        return;
    console.log("color changed by hsv_h_range");
    let hsv = get_HSV();
    color = HSV_to_HEX(h, hsv.s, hsv.v);
    sync_colors();
}

function hsv_s_change() {
    let s = parseInt($('#hsv_s_input').val());
    if (s < 0 || s > 100 || isNaN(s))
        return;
    console.log("color changed by hsv_s_input");
    let hsv = get_HSV();
    color = HSV_to_HEX(hsv.h, s, hsv.v);
    sync_colors();
}

function hsv_s_range_change() {
    let s = parseInt($('#hsv_s_range').val());
    if (s < 0 || s > 100 || isNaN(s))
        return;
    console.log("color changed by hsv_s_range");
    let hsv = get_HSV();
    color = HSV_to_HEX(hsv.h, s, hsv.v);
    sync_colors();
}

function hsv_v_change() {
    let v = parseInt($('#hsv_v_input').val());
    if (v < 0 || v > 100 || isNaN(v))
        return;
    console.log("color changed by hsv_v_input");
    let hsv = get_HSV();
    color = HSV_to_HEX(hsv.h, hsv.s, v);
    sync_colors();
}

function hsv_v_range_change() {
    let v = parseInt($('#hsv_v_range').val());
    if (v < 0 || v > 100 || isNaN(v))
        return;
    console.log("color changed by hsv_v_range");
    let hsv = get_HSV();
    color = HSV_to_HEX(hsv.h, hsv.s, v);
    sync_colors();
}

function xyz_x_change() {
    let x = parseInt($('#xyz_x_input').val());
    if (x < 0 || x > 100 || isNaN(x))
        return;
    console.log("color changed by xyz_x_input");
    let xyz = get_XYZ();
    color = XYZ_to_HEX(x, xyz.y, xyz.z);
    sync_colors();
}

function xyz_x_range_change() {
    let x = parseInt($('#xyz_x_range').val());
    if (x < 0 || x > 100 || isNaN(x))
        return;
    console.log("color changed by xyz_x_range");
    let xyz = get_XYZ();
    color = XYZ_to_HEX(x, xyz.y, xyz.z);
    sync_colors();
}

function xyz_y_change() {
    let y = parseInt($('#xyz_y_input').val());
    if (y < 0 || y > 100 || isNaN(y))
        return;
    console.log("color changed by xyz_y_input");
    let xyz = get_XYZ();
    color = XYZ_to_HEX(xyz.x, y, xyz.z);
    sync_colors();
}

function xyz_y_range_change() {
    let y = parseInt($('#xyz_y_range').val());
    if (y < 0 || y > 100 || isNaN(y))
        return;
    console.log("color changed by xyz_y_range");
    let xyz = get_XYZ();
    color = XYZ_to_HEX(xyz.x, y, xyz.z);
    sync_colors();
}

function xyz_z_change() {
    let z = parseInt($('#xyz_z_input').val());
    if (z < 0 || z > 100 || isNaN(z))
        return;
    console.log("color changed by xyz_z_input");
    let xyz = get_XYZ();
    color = XYZ_to_HEX(xyz.x, xyz.y, z);
    sync_colors();
}

function xyz_z_range_change() {
    let z = parseInt($('#xyz_z_range').val());
    if (z < 0 || z > 100 || isNaN(z))
        return;
    console.log("color changed by xyz_z_range");
    let xyz = get_XYZ();
    color = XYZ_to_HEX(xyz.x, xyz.y, z);
    sync_colors();
}

function lab_l_change() {
    let l = parseInt($('#lab_l_input').val());
    if (l < 0 || l > 100 || isNaN(l))
        return;
    console.log("color changed by lab_l_input");
    let lab = get_LAB();
    color = LAB_to_HEX(l, lab.a, lab.b);
    sync_colors();
}

function lab_l_range_change() {
    let l = parseInt($('#lab_l_range').val());
    if (l < 0 || l > 100 || isNaN(l))
        return;
    console.log("color changed by lab_l_range");
    let lab = get_LAB();
    color = LAB_to_HEX(l, lab.a, lab.b);
    sync_colors();
}

function lab_a_change() {
    let a = parseInt($('#lab_a_input').val());
    if (a < -128 || a > 127 || isNaN(a))
        return;
    console.log("color changed by lab_a_input");
    let lab = get_LAB();
    color = LAB_to_HEX(lab.l, a, lab.b);
    sync_colors();
}

function lab_a_range_change() {
    let a = parseInt($('#lab_a_range').val());
    if (a < -128 || a > 127 || isNaN(a))
        return;
    console.log("color changed by lab_a_range");
    let lab = get_LAB();
    color = LAB_to_HEX(lab.l, a, lab.b);
    sync_colors();
}

function lab_b_change() {
    let b = parseInt($('#lab_b_input').val());
    if (b < -128 || b > 127 || isNaN(b))
        return;
    console.log("color changed by lab_b_input");
    let lab = get_LAB();
    color = LAB_to_HEX(lab.l, lab.a, b);
    sync_colors();
}

function lab_b_range_change() {
    let b = parseInt($('#lab_b_range').val());
    if (b < -128 || b > 127 || isNaN(b))
        return;
    console.log("color changed by lab_b_range");
    let lab = get_LAB();
    color = LAB_to_HEX(lab.l, lab.a, b);
    sync_colors();
}
// endregion

window.onload = function () {
    sync_colors();
}
