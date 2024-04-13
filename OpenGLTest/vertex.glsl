#version 330 core

layout(location = 0) in vec3 a_Pos;
layout(location = 1) in vec3 a_Col;
layout(location = 2) in vec2 ccc;

uniform mat4 uPer;
uniform mat4 uMo;
uniform mat4 uV;
uniform mat2 trasnpose;

out vec4 vertexColor;
out vec2 vTexCoord;

void main()
{
   gl_Position = uPer * uV * uMo * vec4(a_Pos, 1.0f);
   vertexColor = vec4(a_Col, 1.0f);
   vTexCoord = ccc;
}