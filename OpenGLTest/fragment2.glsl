#version 330 core
//const vec3 lightColor = vec3(0.8, 0.8, 0.8);
//const vec3 lightPosition = vec3(5.0, 7.0, 2.0);
//const vec3 ambientLight = vec3(0.3, 0.3, 0.3);

in vec4 vertexColor;
in vec2 vTexCoord;

uniform sampler2D uSampler;

out vec4 FragColor;

void main()
{
    FragColor = vec4(texture(uSampler, vTexCoord)) * vec4(vertexColor);
//    FragColor = vec4(vertexColor);
}