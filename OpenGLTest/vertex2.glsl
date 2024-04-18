#version 330 core

layout(location = 0) in vec3 a_Pos;
layout(location = 1) in vec3 a_Nor;
layout(location = 2) in vec2 a_Tex;

uniform mat4 uMVP;

out vec4 vertexColor;
out vec2 vTexCoord;

void main()
{
   gl_Position = uMVP * vec4(a_Pos, 1.0f);
   vertexColor = vec4(a_Nor, 1.0f);
   vTexCoord = a_Tex;
}