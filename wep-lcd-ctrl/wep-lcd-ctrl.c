/*
 * wep-lcd-ctrl.c
 *
 * Copyright (C) 2003 ETC s.r.o.
 *
 * Simple command line tool for changing contrast and intensity of LCD
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * Written by Peter Figuli <peposh@etc.sk>, 2003
 *
 */

#include "stdio.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "lcdctrl.h"


static const char *opt_backlight = NULL;
static const char *opt_brightnes = NULL;
static const char *opt_contrast  = NULL;


static void help( void );
static void backlight( void );
static void brightness( void );
static void contrast( void );
static void on( void );
static void off( void );

static int fd;

static struct {
  const char *name;
  const char **value;
  const char *description;
  void ( *func)(void );
  int used;
} option[]={
  { "--help", NULL,           "       -displays this help",                 help,      0 },
  { "-br",    &opt_brightnes, "[<0,100>] -display/Set brightness",          brightness,1 },
  { "-bl",    &opt_backlight, "[<0,100>] -display/Set backlight intensity", backlight, 1 },
  { "-co",    &opt_contrast,  "[<0,100>] -display/Set contrast",            contrast,  1 },
  { "-on",     NULL,           "           -turn display ON",                on,        0 },
  { "-off",    NULL,           "          -turn display OFF",                off,       0 },
  { NULL,     NULL,           NULL,                                         NULL,      0 }
};

static void help( void ){
  int i;

  printf( "Usage\n" );
  for( i = 0; option[ i ].name != NULL; i++ ){
    printf( "  %s %s\n", option[ i ].name, option[ i ].description );
  }
  printf( "\n\n" );
}

int getValue( const char *value ){
  int result;

  result = atoi( value );
  return result > 100? 100: result < 0? 0: result;
}

static void backlight( void ){
  if( opt_backlight != NULL ){
    ioctl( fd,  _LCDCTRL_IOCTL_INTENSITY, getValue( opt_backlight ));
  }else{
    printf( " Backlight: %d\n", ioctl( fd, _LCDCTRL_IOCTL_GET_INTENSITY ));
  }
}

static void brightness( void ){
  if( opt_brightnes != NULL ){
    ioctl( fd,  _LCDCTRL_IOCTL_BRIGHTNESS, getValue( opt_brightnes ));
  }else{
    printf( "Brightness: %d\n", ioctl( fd, _LCDCTRL_IOCTL_GET_BRIGHTNESS ));
  }
}

static void contrast( void ){
  if( opt_contrast != NULL ){
    ioctl( fd,  _LCDCTRL_IOCTL_CONTRAST, getValue( opt_contrast ));
  }else{
    printf( "  Contrast: %d\n", ioctl( fd, _LCDCTRL_IOCTL_GET_CONTRAST ));
  }
}

static void on( void ){
  ioctl( fd, _LCDCTRL_IOCTL_ON );
}
static void off( void ){
  ioctl( fd, _LCDCTRL_IOCTL_OFF );
}

int
main( int argc, char **argv ){
  int i, used;

  if(( fd = open( "/dev/lcdctrl", O_RDONLY )) == -1 ){
    printf( "Unable to open lcdctrl driver\n" );
    exit( 1 );
  }

  if( argc > 1 ){
    for( i = 0 ; option[ i ].name; i++ ){
      option[ i ].used = 0;
    }
  }

  while( --argc > 0 ){
    argv++;
    for( i = 0; option[ i ].name != NULL; i++ ){
      if( !strcmp( argv[ 0 ], option[ i ].name )){
	option[ i ].used = 1;
	if( argc > 1 ){
	  if( !strchr( argv[ 1 ], '-' )){
	    argv++; argc--;
	    *option[ i ].value = argv[ 0 ];
	  }
	}
	break;
      }
    } 
  }

  used = 0;
  for( i = 0; option[ i ].name != NULL; i++ ){
    if( option[ i ].used ){
      used++;
      option[ i ].func();
    }
  }
  if( !used ){
    help();
  }
}

