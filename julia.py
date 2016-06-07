from __future__ import division
import scene

shader_text = """
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

#define iResolution u_sprite_size
#define iGlobalTime u_time

// Created by inigo quilez - iq/2013
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
// https://www.shadertoy.com/view/Mss3R8
// learn more here: // http://www.iquilezles.org/www/articles/distancefractals/distancefractals.htm

float calc( vec2 p, float time )
{
	p = -1.0 + 2.0*p;
	p.x *= iResolution.x/iResolution.y;

	float ltime = 0.5-0.5*cos(time*0.12);
    float zoom = pow( 0.9, 100.0*ltime );
	float an = 2.0*ltime;
	p = mat2(cos(an),sin(an),-sin(an),cos(an))*p;
	vec2 ce = vec2( 0.2655,0.301 );
	ce += zoom*0.8*cos(4.0+4.0*ltime);
	p = ce + (p-ce)*zoom;
	vec2 c = vec2( -0.745, 0.186 ) - 0.045*zoom*(1.0-ltime);

	vec2 z = p;
	vec2 dz = vec2( 1.0, 0.0 );

	for( int i=0; i<256; i++ )
	{
		dz = 2.0*vec2(z.x*dz.x-z.y*dz.y, z.x*dz.y + z.y*dz.x );
        z = vec2( z.x*z.x - z.y*z.y, 2.0*z.x*z.y ) + c;
		if( dot(z,z)>200.0 ) break;
	}

	float d = sqrt( dot(z,z)/dot(dz,dz) )*log(dot(z,z));

	return pow( clamp( (150.0/zoom)*d, 0.0, 1.0 ), 0.5 );
}


void main(void)
{
	vec2 uv = v_tex_coord;
	#if 0
	float scol = calc( uv, iGlobalTime );
    #else

    float scol = 0.0;
	for( int j=0; j<2; j++ )
	for( int i=0; i<2; i++ )
	{
		vec2 of = -0.5 + vec2( float(i), float(j) ) / 2.0;
        of = (of/iResolution.xy);
	    scol += calc(uv+of, iGlobalTime );
	}
	scol *= 0.25;

    #endif

	vec3 vcol = pow( vec3(scol), vec3(0.9,1.1,1.4) );


	vcol *= 0.7 + 0.3*pow(16.0*uv.x*uv.y*(1.0-uv.x)*(1.0-uv.y),0.25);


	gl_FragColor = vec4( vcol, 1.0 );
}

"""

class MyScene (scene.Scene):
    def setup(self):
        im = scene.load_image_file('snake.png')
        self.sprite = scene.SpriteNode(im, size=(512, 512), parent=self)
        self.sprite.shader = scene.Shader(shader_text)
        self.sprite.position = (self.size[0]/2.0, self.size[1]/2.0)

scene.run(MyScene(), show_fps=True)
